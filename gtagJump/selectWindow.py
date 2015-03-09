#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
from gi.repository import Gtk, Gio, Gdk


class TreeViewWithColumn(Gtk.TreeView):
    # コラム内の項目番号(連番)をrange()で作成する
    (
        COLUMN_FILE,
        COLUMN_LINE,
        COLUMN_LINE_STR,
    ) = range(3)    # 実際の値は上から順に0,1,2が入る

    def __init__(self, *args, **kwargs):
        Gtk.TreeView.__init__(self, *args, **kwargs)    # 必須
        self.col_file = Gtk.TreeViewColumn('File', Gtk.CellRendererText(), text=self.COLUMN_FILE)
        self.col_line = Gtk.TreeViewColumn('Line', Gtk.CellRendererText(), text=self.COLUMN_LINE)
        self.col_line_str = Gtk.TreeViewColumn('', Gtk.CellRendererText(), text=self.COLUMN_LINE_STR)
        self.append_column(self.col_file)
        self.append_column(self.col_line)
        self.append_column(self.col_line_str)


class SelectWindow(Gtk.Window):
    def __init__(self, plugin, windowTitle, recodes):
        Gtk.Window.__init__(self)
        self.plugin = plugin
        self.treeview = TreeViewWithColumn(
            model=Gtk.ListStore(str, int, str)
        )  # file, line, line_str
        self.treeview.set_rules_hint(True)
        self.connect("key-press-event", self.__enter)
        self.connect("button-press-event", self.__enter)
        sw = Gtk.ScrolledWindow()
        sw.add(self.treeview)
        for rec in recodes:
            if rec is not None:
                self.treeview.get_model().append(rec)
        self.add(sw)
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
            model, iter = self.treeview.get_selection().get_selected()
            path, line, line_str = model.get(
                iter,
                self.treeview.COLUMN_FILE,
                self.treeview.COLUMN_LINE,
                self.treeview.COLUMN_LINE_STR
            )
            self.destroy()
            self.plugin.open_location(Gio.File.new_for_path(path), line)


class MockPlugin:
    def open_location(self, f, l):
        print(f.get_path())
        print(l)
        Gtk.main_quit()


def main():
    window = SelectWindow(MockPlugin(), "test", [
        ("testfile.py", 10, "def testfunc():"),
        ("testfile.py", 10, "def testfunc():"),
    ])
    window.show_all()
    Gtk.main()
    return 0
if __name__ == '__main__':
    sys.exit(main())
