# -*- coding: utf-8 -*-
import zmarkdown
import re


class DownHeaderExtension(zmarkdown.Extension):
    def __init__(self, *args, **kwargs):
        self.config = {"offset": [1, "header offset to apply"]}
        zmarkdown.Extension.__init__(self, *args, **kwargs)

    def extendZMarkdown(self, md, md_globals):
        # VERY DANGEROUS !
        md.parser.blockprocessors["hashheader"].RE = re.compile(
            r'(^|\n)(?P<level>#{1,%d})(?P<header>.*?)#*(\n|$)' % (6 - self.getConfig("offset")))
        md.treeprocessors.add('downheader', DownHeaderProcessor(self.getConfig("offset")), '_end')


class DownHeaderProcessor(zmarkdown.treeprocessors.Treeprocessor):
    def __init__(self, offset=1):
        zmarkdown.treeprocessors.Treeprocessor.__init__(self)
        self.offset = offset

    def run(self, node):
        expr = re.compile('h(\d)')
        for child in node.getiterator():
            match = expr.match(child.tag)
            if match:
                child.tag = 'h' + str(min(6, int(match.group(1)) + self.offset))
        return node
