# Emoticon extension for python-markdown
# Original version :
# https://gist.github.com/insin/815656/raw/a68516f1ffc03df465730b3ddef6de0a11b7e9a5/mdx_emoticons.py
#
# Patched by cgabard for supporting newer python-markdown version and extend for support multi-extensions

import re
import zmarkdown
from zmarkdown.inlinepatterns import Pattern
from zmarkdown.util import etree


class EmoticonExtension(zmarkdown.Extension):
    def __init__(self, *args, **kwargs):
        self.config = {
            'emoticons': [{
                ":)": "test.png",
            }, 'A mapping from emoticon symbols to image names.'],
        }

        zmarkdown.Extension.__init__(self, *args, **kwargs)

    def extendZMarkdown(self, md, md_globals):
        self.md = md
        emoticons = self.getConfig('emoticons')
        if emoticons:
            EMOTICON_RE = u'(^|(?<=\s))(?P<emoticon>{0})((?=\s)|$)'.format(
                '|'.join([re.escape(emoticon) for emoticon in emoticons.keys()]))
            md.inlinePatterns.add('emoticons', EmoticonPattern(EMOTICON_RE, emoticons), "<linebreak")


class EmoticonPattern(Pattern):
    def __init__(self, pattern, emoticons):
        Pattern.__init__(self, pattern)
        self.emoticons = emoticons

    def handleMatch(self, m):
        try:
            emoticon = m.group('emoticon')
            if emoticon not in self.emoticons:
                return None
        except IndexError:  # pragma: no cover
            return None
        el = etree.Element('img')
        el.set('src', '%s' % (self.emoticons[emoticon],))
        el.set('alt', emoticon)
        return el


def makeExtension(*args, **kwargs):
    return EmoticonExtension(*args, **kwargs)
