# -*- coding: utf-8 -*-

from collections import deque
import os

from gi.repository import GObject, Gedit, Gio

from gtagJump import selectWindow, settings


def getCurrentIdentifier(doc):
    s = doc.get_iter_at_mark(doc.get_insert())
    e = s.copy()
    while True:
        back = s.copy()
        if not back.backward_char():
            break
        c = back.get_char()
        if not (c.isalpha() or c == '_' or c.isdigit()):
            break
        s.backward_char()
    if s.get_char().isdigit():
        return None
    while True:
        c = e.get_char()
        if not (c.isalpha() or c == '_' or c.isdigit()):
            break
        if not e.forward_char():
            break
    return s.get_text(e)


ACTION_DEFS = [
    ("gtagJumpDef", "Jump Def", settings.keyJumpDef),
    ("gtagJumpRef", "Jump Ref", settings.keyJumpRef),
    ("gtagJumpBack", "Jump Back", settings.keyJumpBack),
    ("gtagJumpNext", "Jump Next", settings.keyJumpNext),
]


class GtagJumpAppActivatable(GObject.Object, Gedit.AppActivatable):

    app = GObject.property(type=Gedit.App)

    def do_activate(self):
        self.menu_ext = self.extend_menu("tools-section")
        for name, title, key in ACTION_DEFS:
            accelerator = "win." + name
            self.app.add_accelerator(key, accelerator, None)
            item = Gio.MenuItem.new(_(title), accelerator)
            self.menu_ext.append_menu_item(item)

    def do_deactivate(self):
        for action_def in ACTION_DEFS:
            accelerator = "win." + action_def[0]
            self.app.remove_accelerator(accelerator, None)
        self.menu_ext = None


class GtagJumpWindowActivatable(GObject.Object, Gedit.WindowActivatable):
    __gtype_name = "GtagJump"
    window = GObject.property(type=Gedit.Window)
    backstack = deque()
    nextstack = deque()

    def do_activate(self):
        slots = {
            "gtagJumpDef": self.__jump_def,
            "gtagJumpRef": self.__jump_ref,
            "gtagJumpBack": self.__back,
            "gtagJumpNext": self.__next,
        }
        for name, title, key in ACTION_DEFS:
            action = Gio.SimpleAction(name=name)
            action.connect('activate', slots[name])
            self.window.add_action(action)

    def do_deactivate(self):
        for name, title, key in ACTION_DEFS:
            self.window.remove_action(name)

    def do_update_state(self):
        pass

    def __jump(self, navi_method):
        doc = self.window.get_active_document()
        identifier = getCurrentIdentifier(doc)
        refs = []
        for navi in settings.navigator:
            try:
                refs += navi_method(navi)(doc, identifier)
            except TypeError:
                continue
        self.add_history(self.backstack)
        self.jump(refs, identifier)

    def __jump_def(self, action, dummy):
        self.__jump(lambda navi: navi.getDefinitions)

    def __jump_ref(self, action, dummy):
        self.__jump(lambda navi: navi.getReferences)

    def __back(self, action, dummy):
        try:
            preLocation = self.backstack.pop()
        except IndexError:
            return
        self.add_history(self.nextstack)
        self.open_location(preLocation[0], preLocation[1])

    def __next(self, action, dummy):
        try:
            nextLocation = self.nextstack.pop()
        except IndexError:
            return
        self.add_history(self.backstack)
        self.open_location(nextLocation[0], nextLocation[1])

    def jump(self, locations, identifier):
        """
        locations: [(Gio.File, int)] or [(str, int), ...]
        """

        def location_opener(location):
            path, line, code, doc_path = location
            if isinstance(path, Gio.File):
                gio_file = path
            else:
                dirname = os.path.dirname(doc_path)
                newpath = os.path.normpath(os.path.join(dirname, path))
                gio_file = Gio.File.new_for_path(newpath)
            self.open_location(gio_file, line)

        if len(locations) == 1:
            location_opener(locations[0])
        elif len(locations) > 1:
            locations.sort()
            window = selectWindow.SelectWindow(
                self,
                identifier,
                locations,
                location_opener
            )
            window.show_all()

    def add_history(self, stack):
        doc = self.window.get_active_document()
        stack.append((
            doc.get_location(),
            doc.get_iter_at_mark(doc.get_insert()).get_line() + 1
        ))
        if len(stack) == settings.historymax:
            stack.popleft()

    def open_location(self, location, line):
        for d in self.window.get_documents():
            if d.get_location().equal(location):
                tab = Gedit.Tab.get_from_document(d)
                self.window.set_active_tab(tab)
                d.goto_line(line - 1)
                self.window.get_active_view().scroll_to_cursor()
                break
        else:
            # file has not opened yet
            self.window.create_tab_from_location(location, None, line, 0, False, True)
