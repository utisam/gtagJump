# -*- coding:utf-8 -*-

import os
import re
import subprocess


class GtagsNavigator:
    def _call_global(self, doc, identifier, param):
        cwd = os.getcwd()
        try:
            doc_path = os.path.dirname(doc.get_location().get_path())
            os.chdir(doc_path)
            text = subprocess.check_output(
                ["/usr/bin/global", "--encode-path", " ", param, identifier]
            ).decode('utf8')
            os.chdir(cwd)
            for line in text.split('\n'):
                matchObj = re.search(
                    "^" + identifier + " +([0-9]+) +([^ ]+) +(.*)",
                    line
                )
                if not matchObj:
                    continue

                lineno, path, code = matchObj.groups()
                path = path.replace('%20', ' ')
                yield path, int(lineno), code, doc.get_location().get_path()
        except OSError:
            pass
        finally:
            os.chdir(cwd)

    def getDefinitions(self, doc, identifier):
        yield from self._call_global(doc, identifier, '-x')

    def getReferences(self, doc, identifier):
        yield from self._call_global(doc, identifier, '-rx')
