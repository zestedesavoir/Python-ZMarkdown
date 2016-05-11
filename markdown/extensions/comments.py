# Comment extension
# inspired by  https://github.com/ryneeverett/python-markdown-comments

import re
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension


class CommentsExtension(Extension):
    def __init__(self, *args, **kwargs):
        self.config = {"start_tag": ["<--COMMENTS", ""],
                       "end_tag":   ["COMMENTS-->", ""]}
        Extension.__init__(self, *args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors.add("comments",
                             CommentsProcessor(md, self.getConfig("start_tag"), self.getConfig("end_tag")),
                             ">fenced_code_block")


class CommentsProcessor(Preprocessor):
    def __init__(self, md, start_tag, end_tag):
        Preprocessor.__init__(self, md)

        StaEsc = re.escape(start_tag)
        EndEsc = re.escape(end_tag)

        self.RE = re.compile(StaEsc + r'.*?' + EndEsc, re.MULTILINE | re.DOTALL)

    def run(self, lines):
        text = "\n".join(lines)
        while True:
            m = self.RE.search(text)
            if m:
                text = "%s%s" % (text[:m.start()], text[m.end():])
            else:
                break
        return text.split("\n")


def makeExtension(*args, **kwargs):
    return CommentsExtension(*args, **kwargs)
