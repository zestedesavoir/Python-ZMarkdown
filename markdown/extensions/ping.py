import markdown
from markdown.inlinepatterns import Pattern

# (?<![^\s]) # Check that there isn't any space before the ping
# @(?:
#   ([-_\d\w]+) # For @ping
# |
#   \[ # For @[ping long]
#     ([^\[\]\n]+) # Match everything excepted [, ] and \n
#   \]
# )

PING_RE = r'(?<![^\s])@(?:([-_\d\w]+)|\[([^\[\]\n]+)\])'


class PingPattern(Pattern):
    def __init__(self, pattern, is_pinged):
        Pattern.__init__(self, pattern)
        self.is_pinged = is_pinged

    def handleMatch(self, m):
        if self.is_pinged(m.group(2)):
            index = 2
        elif self.is_pinged(m.group(3)):
            index = 3
        else:
            return None
        dnode = markdown.util.etree.Element('a')
        dnode.set('class', 'ping')
        dnode.set('href', '/membres/voir/{}/'.format(m.group(index)))
        dnode.text = markdown.util.AtomicString('@{}'.format(m.group(index)))
        return dnode


class PingExtension(markdown.extensions.Extension):
    """Adds ping extension to Markdown class."""

    def __init__(self, is_pinged, configs={}):
        super(PingExtension, self).__init__()
        self.is_pinged = is_pinged
        for key, value in configs:
            self.setConfig(key, value)

    def extendMarkdown(self, md, md_globals):
        """Modifies inline patterns."""
        md.inlinePatterns.add('a', PingPattern(PING_RE, self.is_pinged),
                              '<not_strong')  # no idea what is this last parameter.


def makeExtension(configs={}):
    def is_pinged(user=None):
        return False

    return PingExtension(is_pinged, configs=dict(configs))
