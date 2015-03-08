# -*- coding:utf-8 -*-

import symtable


class PythonNavigator:
    def getDefinitions(self, doc, identifier):
        if doc.get_language().get_name() != "Python":
            return
        with open(doc.get_location().get_path()) as f:
            table = symtable.symtable(
                f.read(),
                doc.get_location().get_basename(),
                "exec",
            )
            for line in self.generateDefLines(table, identifier):
                yield (doc.get_location(), line, "")

    def generateDefLines(self, table, identifier):
        for c in table.get_children():
            if c.get_name() == identifier:
                yield c.get_lineno()
            for l in self.generateDefLines(c, identifier):
                yield l

    def getReferences(self, doc, identifier):
        pass
