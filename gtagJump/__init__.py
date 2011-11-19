#-*- coding:utf-8 -*-
import os
import re
import subprocess
import urlparse
import gio
import gtk
import gedit
import selectWindow

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

def getLinesOfIdentifier(identifier, rOption=False):
	command = ["global", "-x"]
	if rOption:
		command.append("-r")
	command.append(identifier)
	ps_global = subprocess.Popen(command, stdout=subprocess.PIPE)
	result = []
	try:
		for line in ps_global.stdout:
			#print line,
			result.append(line[0: -1])
	finally:		
		ps_global.stdout.close()
	return result

def resultLineToLocation(identifier, line):
	matchObj = re.search("^" + identifier + " +[0-9]+", line)
	if matchObj is None:
		return None, None
	l = int(matchObj.group(0)[len(identifier):])
	matchObj = re.search("^ *[^ ]+ *", line[matchObj.end():])
	if matchObj is None:
		return None, None
	path = matchObj.group(0).strip()
#	print path + " " + str(l)
	return path, l

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

class GtagJump(gedit.Plugin):
	def __init__(self):
		gedit.Plugin.__init__(self)
	def activate(self, window):
		global ui_str
		self.geditWindow = window
		manager = window.get_ui_manager()
		self.action_group = gtk.ActionGroup("gflyPluginAction")
		self.action_group.add_actions([
				("gtagJumpDef", None, "Jump Def", "F3", None, self.__jump_def),
				("gtagJumpRef", None, "Jump Ref", "<Control>F3", None, self.__jump_ref)
			])
		manager.insert_action_group(self.action_group, -1)
		self.ui_id = manager.add_ui_from_string(ui_str)
	def deactivate(self, window):
		pass
	def update_ui(self, window):
		self.geditWindow = window
	def __jump_def(self, action):
		self.globalJump()
	def __jump_ref(self, action):
		self.globalJump(True)
	def globalJump(self, rOpt=False):
		view = self.geditWindow.get_active_view()
		doc = view.get_buffer()
		identifier = getCurrentIdentifier(doc)
		if identifier is None:
			return
		lines = getLinesOfIdentifier(identifier, rOpt)
#		print "selections count = " + str(len(lines))
		if len(lines) == 1:
			path, l = resultLineToLocation(identifier, lines[0])
			selectWindow.openFileLine(self.geditWindow, path, l)
		elif 1 < len(lines):
			selectWindow.show(identifier, lines, self.geditWindow)
