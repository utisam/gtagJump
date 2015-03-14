#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from gi.repository import Gtk, Gdk


class TreeViewWithColumn(Gtk.TreeView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    # 必須
        for i, head in enumerate(['File', 'Line', '', '']):
            col = Gtk.TreeViewColumn(head, Gtk.CellRendererText(), text=i)
            self.append_column(col)
        col.set_visible(False)


class SelectWindow(Gtk.Window):
    def __init__(self, plugin, windowTitle, records, opener):
        Gtk.Window.__init__(self)
        self.plugin = plugin
        self.treeview = TreeViewWithColumn(
            model=Gtk.ListStore(str, int, str, str)
        )  # file, line, line_str
        self.treeview.set_rules_hint(True)
        self.connect("key-press-event", self.__enter)
        self.connect("button-press-event", self.__enter)
        sw = Gtk.ScrolledWindow()
        sw.add(self.treeview)
        for rec in records:
            if rec is not None:
                self.treeview.get_model().append(rec)
        self.add(sw)
        self.opener = opener
        self.set_title(windowTitle)
        self.set_size_request(700, 360)

    def __enter(self, w, e):
        event_type = e.get_event_type()
        if (
            event_type == Gdk.EventType._2BUTTON_PRESS
            or (
                event_type == Gdk.EventType.KEY_PRESS
                and e.keyval == 65293
            )
        ):
            model, tree_iter = self.treeview.get_selection().get_selected()
            location = model.get(tree_iter, 0, 1, 2, 3)
            self.destroy()
            self.opener(location)


class MockPlugin:
    def open_location(self, f, l):
        print(f.get_path())
        print(l)
        Gtk.main_quit()


def main():
    window = SelectWindow(MockPlugin(), "test", [
        (10, "testfile.py", "def testfunc():", "not visible"),
        (10, "testfile.py", "def testfunc():", "not visible"),
    ])
    window.show_all()
    Gtk.main()
    return 0
if __name__ == '__main__':
    sys.exit(main())
