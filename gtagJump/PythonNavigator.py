# -*- coding:utf-8 -*-

import symtable


class PythonNavigator:
    def getDefinitions(self, doc, identifier):
        if doc.get_language().get_name() != "Python":
            return
        doc_location = doc.get_location()
        with open(doc_location.get_path()) as f:
            table = symtable.symtable(
                f.read(),
                doc_location.get_basename(),
                "exec",
            )
            for line in self.generateDefLines(table, identifier):
                yield doc_location, line, "", doc_location.get_path()

    def generateDefLines(self, table, identifier):
        for c in table.get_children():
            if c.get_name() == identifier:
                yield c.get_lineno()
            yield from self.generateDefLines(c, identifier)

    def getReferences(self, doc, identifier):
        pass
