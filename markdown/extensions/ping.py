import markdown
from markdown.inlinepatterns import Pattern

PING_RE = (r'(?<![^\s])'  # Check that there isn't any space before the ping
           r'@(?:'
           r'([-_\d\w]+)'  # For @ping
           r'|'
           r'\['  # For @[ping long]
           r'([^\[\]\n]+)'  # Match everything excepted [, ] and \n
           r'\]'
           r')')


class PingPattern(Pattern):
    def __init__(self, md, is_pingeable):
        self.is_pingeable = is_pingeable
        Pattern.__init__(self, PING_RE, md)

    def handleMatch(self, m):
        if self.is_pingeable(m.group(2)):
            name = m.group(2)
        elif self.is_pingeable(m.group(3)):
            name = m.group(3)
        else:
            return None
        dnode = markdown.util.etree.Element('a')

        dnode.set('class', 'ping')
        dnode.set('href', '/membres/voir/{}/'.format(name))
        dnode.text = markdown.util.AtomicString('@{}'.format(name))
        self.markdown.metadata["ping"].add(name)
        return dnode


class PingExtension(markdown.extensions.Extension):
    """Adds ping extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        self.config = {
            "is_pingeable": [lambda _: False, 'Function that should return True if it is a valid pingeable name']}
        super(PingExtension, self).__init__(*args, **kwargs)

    def reset(self):
        self.md.metadata["ping"] = set()

    def extendMarkdown(self, md, md_globals):
        """Modifies inline patterns."""
        md.inlinePatterns.add('a', PingPattern(md, self.getConfig('is_pingeable')), '<not_strong')
        self.md = md
        self.reset()
        md.registerExtension(self)
