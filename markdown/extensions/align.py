#! /usr/bin/env python

import markdown
from markdown.blockprocessors import BlockProcessor
import re
from markdown import util


class AlignProcessor(BlockProcessor):
    """ Process Align. """

    def __init__(self, parser):
        BlockProcessor.__init__(self, parser)

        exprs = (("->", "right"), ("<-", "center"))

        self.REStart = re.compile(r'(^|\n)' + re.escape('->'))
        self._ending_re = [re.compile(re.escape(end_expr) + r'(\n|$)') for end_expr, _ in exprs]
        self._kind_align = [kind_align for _, kind_align in exprs]

    def test(self, parent, block):
        return bool(self.REStart.search(block))

    def run(self, parent, blocks):

        FirstBlock = blocks[0]
        m = self.REStart.search(FirstBlock)
        if not m:
            return False
        StartBlock = (0, m.start(), m.end())

        EndBlock = (-1, -1, -1)
        content_align = "left"
        for i in range(len(blocks)):
            if i == 0:
                txt = FirstBlock[m.end() + 1:]
                dec = m.end() - m.start() + 1
            else:
                txt = blocks[i]
                dec = 0
            # Test all ending aligns
            t_ends = ((i, re_end.search(txt)) for i, re_end in enumerate(self._ending_re))
            # Catch only matching re
            t_ends = list(filter(lambda e: e[1] is not None, t_ends))
            if len(t_ends) > 0:
                # retrieve first matching re
                selected_align, mEnd = min(t_ends, key=lambda e: e[1].start())
                EndBlock = (i, mEnd.start() + dec, mEnd.end() + dec)
                content_align = self._kind_align[selected_align]
                break

        if EndBlock[0] < 0:
            return False
        Before = FirstBlock[:StartBlock[1]]
        Content = []
        After = blocks[EndBlock[0]][EndBlock[2]:]
        for i in range(0, EndBlock[0] + 1):
            blck = blocks.pop(0)

            if i == StartBlock[0]:
                startIndex = StartBlock[2]
            else:
                startIndex = 0

            if i == EndBlock[0]:
                endIndex = EndBlock[1]
            else:
                endIndex = len(blck)

            Content.append(blck[startIndex: endIndex])

        Content = "\n\n".join(Content)

        if Before:
            self.parser.parseBlocks(parent, [Before])

        sibling = self.lastChild(parent)
        if (sibling and
                sibling.tag == "div" and
                "align" in sibling.attrib and
                sibling.attrib["align"] == content_align):
            h = sibling

            if h.text:
                h.text += '\n'
        else:
            h = util.etree.SubElement(parent, 'div')
            h.set("align", content_align)

        self.parser.parseChunk(h, Content)

        if After:
            blocks.insert(0, After)


class AlignExtension(markdown.extensions.Extension):
    """Adds align extension to Markdown class."""

    def extendMarkdown(self, md, md_globals):
        """Modifies inline patterns."""
        md.registerExtension(self)
        md.parser.blockprocessors.add('align', AlignProcessor(md.parser), '_begin')


def makeExtension(*args, **kwargs):
    return AlignExtension(*args, **kwargs)
