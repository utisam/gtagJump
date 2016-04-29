# -*- coding:utf-8 -*-


class PythonJediNavigator:
    def _get(self, doc, method):
        if doc.get_language().get_name() != "Python":
            return
        try:
            import jedi
        except ImportError:
            return
        # below True or get_slice might be the correct one
        text = doc.get_text(doc.get_start_iter(), doc.get_end_iter(), False)
        path = doc.get_location().get_path()
        cursor = doc.get_iter_at_mark(doc.get_insert())
        script = jedi.Script(
            source=text,
            line=cursor.get_line() + 1,
            # bytes - or maybe get_line_offset (chars)
            column=cursor.get_line_index(),
            path=path
        )
        for definition in getattr(script, method)():
            if definition.line is None:
                continue
            yield (
                definition.module_path,
                definition.line,
                str(definition.column),
                path
            )

    def getDefinitions(self, doc, identifier):
        yield from self._get(doc, 'goto_definitions')

    def getReferences(self, doc, identifier):
        yield from self._get(doc, 'usages')
