#-*- coding:utf-8 -*-
from gi.repository import GObject, Gedit, Gtk
from gio import File

import selectWindow
import settings

ui_str = """<ui>
	<menubar name="MenuBar">
		<menu name="EditMenu" action="Edit">
			<placeholder name="EditOps_6">
				<menuitem name="gtagJumpDef" action="gtagJumpDef"/>
				<menuitem name="gtagJumpRef" action="gtagJumpRef"/>
			</placeholder>
		</menu>
	</menubar>
</ui>
"""

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

class GtagJump(GObject.Object, Gedit.WindowActivatable):
	__gtype_name__ = "GtagJump"
	window = GObject.property(type=Gedit.Window)
	def __init__(self):
		GObject.Object.__init__(self)
	def do_activate(self):
		manager = self.window.get_ui_manager()
		self._action_group = Gtk.ActionGroup("GtagJumpActions")
		actions = [
			("gtagJumpDef", None, "Jump Def", settings.keyJumpDef, None, self.__jump_def),
			("gtagJumpRef", None, "Jump Ref", settings.keyJumpRef, None, self.__jump_ref)
		]
		self._action_group.add_actions(actions)
		manager.insert_action_group(self._action_group, -1)
		self._ui_id = manager.add_ui_from_string(ui_str)
	def do_deactivate(self):
		manager = self.window.get_ui_manager()
		manager.remove_ui(self._ui_id)
		manager.remove_action_group(self._action_group)
		manager.ensure_update()
	def do_update_state(self):
		pass
	def __jump_def(self, action):
		doc = self.window.get_active_document()
		identifier = getCurrentIdentifier(doc)
		print identifier
		defs = []
		for navi in settings.navigator:
			try:
				defs = defs + [d for d in navi.getDefinitions(doc, identifier)]
			except TypeError:
				continue
		self.jump(defs, identifier)
	def __jump_ref(self, action):
		doc = self.window.get_active_document()
		identifier = getCurrentIdentifier(doc)
		print identifier
		refs = []
		for navi in settings.navigator:
			try:
				refs = refs + [d for d in navi.getReferences(doc, identifier)]
			except TypeError:
				continue
		self.jump(refs, identifier)
	def jump(self, locations, identifier):
		if len(locations) != 0:
			if len(locations) == 1:
				if isinstance(locations[0][0], File):
					location = locations[0][0]
				else:
					location = File(locations[0][0])
				line = locations[0][1]
				self.open_location(location, line)
			elif len(locations) > 1:
				window = selectWindow.SelectWindow(self, identifier, locations)
				window.show_all()
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

