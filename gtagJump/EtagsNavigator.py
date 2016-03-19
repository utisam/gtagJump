# -*- coding:utf-8 -*-

import os
from collections import defaultdict


def read_etags(path):
    cur_path = path
    etags = None
    while 1:
        try:
            etags = open(cur_path + '/TAGS', 'r')
            break
        except FileNotFoundError:
            cur_path, prev_dir = os.path.split(cur_path)
            if not prev_dir:
                return None
    data = etags.read().split('\x0c')
    defs = defaultdict(list)
    if data[0]:
        raise Exception("etags TAGS should start with x0c")
    for section in data[1:]:
        lines = section.split('\n')
        if len(lines) < 3:
            raise Exception("etags TAGS section should have at least 3 lines")
        if lines[-1]:
            raise Exception(
                "etags TAGS data lines should have end of line character"
            )
        if lines[0]:
            raise Exception("etags TAGS should have x0c on separate line")
        filename, data_size = lines[1].rsplit(',', 1)
        if not data_size.isdigit():
            raise Exception("etags TAGS data_size should be integer number")
        for line in lines[2:-1]:
            tag_definition, rest = line.split('\x7f', 1)
            tag_definition = tag_definition.strip()
            if '\x01' in rest:
                tagname, location = rest.split('\x01', 1)
            else:
                tagname = tag_definition
                location = rest
            line_number, byte_offset = location.split(',', 1)
            defs[tagname].append((
                cur_path + '/' + filename,
                line_number,
                byte_offset,
                tag_definition
            ))
    return defs


class EtagsNavigator:
    """
    parses etags TAGS format https://en.wikipedia.org/wiki/Ctags#Etags_2
    """

    def getDefinitions(self, doc, identifier):
        doc_path = os.path.dirname(
            os.path.realpath(doc.get_location().get_path())
        )
        for path, lineno, offset, code in read_etags(doc_path)[identifier]:
            yield path, int(lineno), code, doc.get_location().get_path()

    def getReferences(self, doc, identifier):
        pass

