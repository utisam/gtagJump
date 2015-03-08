# -*- coding:utf-8 -*-

import subprocess
import re


class GtagsNavigator:
    def _call_global(self, doc, identifier, param):
        try:
            text = subprocess.check_output(
                ["/usr/bin/global", "--encode-path", " ", param, identifier]
            ).decode('utf8')

            for line in text.split('\n'):
                matchObj = re.search(
                    "^" + identifier + " +([0-9]+) +([^ ]+) +(.*)",
                    line
                )
                if matchObj:
                    lineno, path, code = matchObj.groups()
                    yield path.replace('%20', ' '), int(lineno), code
        except OSError:
            pass

    def getDefinitions(self, doc, identifier):
        yield from self._call_global(doc, identifier, '-x')

    def getReferences(self, doc, identifier):
        yield from self._call_global(doc, identifier, '-rx')
