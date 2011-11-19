#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import re
import gtk
import gio

def openFileLine(geditWindow, path, line):
	def __loaded(doc, arg, view, line):
		doc.goto_line(line - 1)
		view.scroll_to_cursor()
		doc.disconnect(loaded_hadler_id)
	view = geditWindow.get_active_view()
	doc = view.get_buffer()
	gfile = gio.File(os.path.join(os.getcwd(), path))
	if gfile.get_uri() == doc.get_uri():
		doc.goto_line(line - 1)
		view.scroll_to_cursor()
	else:
		view = geditWindow.create_tab_from_uri(gfile.get_uri(), encoding=None, line_pos=line, create=False, jump_to=True).get_view()
		doc = view.get_buffer()
		loaded_hadler_id = doc.connect_after("loaded", __loaded, view, line)

class TreeViewWithColumn(gtk.TreeView):
	"""
	コラムを含んだツリービュー
	"""
	# コラム内の項目番号(連番)をrange()で作成する
	(
		COLUMN_FILE,
		COLUMN_LINE,
		COLUMN_LINE_STR,
	) = range(3)	# 実際の値は上から順に0,1,2が入る
	def __init__(self, *args, **kwargs):
		gtk.TreeView.__init__(self, *args, **kwargs)	# 必須
		self.col_file = gtk.TreeViewColumn('File', gtk.CellRendererText(), text=self.COLUMN_FILE)
		self.col_line = gtk.TreeViewColumn('Line', gtk.CellRendererText(), text=self.COLUMN_LINE)
		self.col_line_str = gtk.TreeViewColumn('', gtk.CellRendererText(), text=self.COLUMN_LINE_STR)
		self.append_column(self.col_file)
		self.append_column(self.col_line)
		self.append_column(self.col_line_str)

class SelectWindow(gtk.Window):
	def __init__(self, identifier, lines, gw):
		gtk.Window.__init__(self)
		self.geditWindow = gw
		self.treeview = TreeViewWithColumn(model=gtk.ListStore(str, int, str))#file, line, line_str
		self.treeview.set_rules_hint(True)
		
		self.connect("key-press-event", self.__enter)
		
		sw = gtk.ScrolledWindow()
		sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
		sw.add(self.treeview)
		
		for line in lines:
			rec = self.createRecode(identifier, line)
			if not rec is None:
				self.treeview.get_model().append(rec)
		
		self.add(sw)
		
		self.set_title(identifier)
		self.set_size_request(640, 160)
	def createRecode(self, identifier, line):
		matchObj = re.search("^" + identifier + " +[0-9]+", line)
		if matchObj is None:
			return None
		l = int(matchObj.group(0)[len(identifier):])
		line_end = matchObj.end()
		matchObj = re.search("^ *[^ ]+ *", line[line_end:])
		if matchObj is None:
			return None
		path = matchObj.group(0).strip()
		return path, l, line[line_end + matchObj.end():]
	def __enter(self, w, e):
		if e.keyval == 65293:
			model, iter = self.treeview.get_selection().get_selected()
			path, line, line_str = model.get(iter, self.treeview.COLUMN_FILE, self.treeview.COLUMN_LINE, self.treeview.COLUMN_LINE_STR)
			self.destroy()
			openFileLine(self.geditWindow, path, line)

def show(identifier, lines, gw):
	window = SelectWindow(identifier, lines, gw)
	window.show_all()
