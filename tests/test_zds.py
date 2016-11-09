from __future__ import unicode_literals
import unittest
import markdown
from markdown.extensions.header_dec import DownHeaderExtension
from markdown.extensions.zds import ZdsExtension
from markdown.extensions.ping import PingExtension


class TestZDSExtensionClass(unittest.TestCase):
    def test_inline_mode(self):
        zds_ext = ZdsExtension(inline=True, emoticons={":D": "image.png"})
        md = markdown.Markdown(extensions=[zds_ext])

        # Basic conversion
        self.assertEqual(
                md.convert('Mon **petit** test *de* text _inline_ avec [un lien](http://www.zestedesavoir.com)'),
                '<p>Mon <strong>petit</strong> test <em>de</em> text <em>'
                'inline</em> avec <a href="http://www.zestedesavoir.com">un lien</a></p>')

        zds_ext = ZdsExtension(inline=True, emoticons={":D": "image.png"})
        md = markdown.Markdown(extensions=[zds_ext])
        # Complex elements should not be allowed
        self.assertEqual(
                md.convert('> ![Image](http://test.com/image.png)'),
                '<p>&gt; ![Image](http://test.com/image.png)\n\n</p>')

    def test_header_dec(self):
        md = markdown.Markdown()
        text_ref = ('# Title 1\n'
                    '## Title 2\n'
                    '### Title 3\n'
                    '#### Title 4\n'
                    '##### Title 5\n'
                    '###### Title 6\n'
                    '####### Title 7\n'
                    'Title 1b\n'
                    '========\n'
                    'Title 2b\n'
                    '--------\n')
        self.assertEqual(
                md.convert(text_ref),
                '<h1>Title 1</h1>\n'
                '<h2>Title 2</h2>\n'
                '<h3>Title 3</h3>\n'
                '<h4>Title 4</h4>\n'
                '<h5>Title 5</h5>\n'
                '<h6>Title 6</h6>\n'
                '<h6># Title 7</h6>\n'
                '<h1>Title 1b</h1>\n'
                '<h2>Title 2b</h2>'
        )
        md = markdown.Markdown(extensions=[DownHeaderExtension(offset=1)])
        self.assertEqual(
                md.convert(text_ref),
                '<h2>Title 1</h2>\n'
                '<h3>Title 2</h3>\n'
                '<h4>Title 3</h4>\n'
                '<h5>Title 4</h5>\n'
                '<h6>Title 5</h6>\n'
                '<h6># Title 6</h6>\n'
                '<h6>## Title 7</h6>\n'
                '<h2>Title 1b</h2>\n'
                '<h3>Title 2b</h3>'
        )
        md = markdown.Markdown(extensions=[DownHeaderExtension(offset=2)])
        self.assertEqual(
                md.convert(text_ref),
                '<h3>Title 1</h3>\n'
                '<h4>Title 2</h4>\n'
                '<h5>Title 3</h5>\n'
                '<h6>Title 4</h6>\n'
                '<h6># Title 5</h6>\n'
                '<h6>## Title 6</h6>\n'
                '<h6>### Title 7</h6>\n'
                '<h3>Title 1b</h3>\n'
                '<h4>Title 2b</h4>'
        )


class TestPing(unittest.TestCase):
    """ Test ping extension. """

    def testNoPing(self):
        """ No ping. """
        md = markdown.Markdown(extensions=[PingExtension()])
        text = 'I want to ping @[Clem].'
        self.assertEqual(
                '<p>I want to ping @[Clem].</p>',
                md.convert(text)
        )
        self.assertEqual(set(), md.metadata["ping"])

    def testPingOneMember(self):
        """ Ping one member when 2 members are specified."""

        def ping_url(user=None):
            if user == 'Clem':
                return '/membres/voir/{}/'.format(user)

        md = markdown.Markdown(extensions=[PingExtension(ping_url=ping_url)])
        text = 'I want to ping @[Clem] and @[Zozor].'
        self.assertEqual(
                '<p>I want to ping <a class="ping" href="/membres/voir/Clem/">@Clem</a> and @[Zozor].</p>',
                md.convert(text)
        )
        self.assertEqual({"Clem"}, md.metadata["ping"])

    def testComplexPing(self):
        """ Complex ping. """

        def ping_url(user=None):
            if user == 'Clem' or user == 'A member':
                return '/membres/voir/{}/'.format(user)

        md = markdown.Markdown(extensions=[PingExtension(ping_url=ping_url)])
        text = 'I want to ping @[Clem], @[Zozor] and @[A member].'
        self.assertEqual(
                '<p>I want to ping <a class="ping" href="/membres/voir/Clem/">@Clem</a>, '
                '@[Zozor] and <a class="ping" href="/membres/voir/A member/">@A member</a>.</p>',
                md.convert(text)
        )
        self.assertEqual({"Clem", "A member"}, md.metadata["ping"])

    def testAllSyntaxes(self):
        """ Test all syntaxes for ping. """

        def ping_url(user=None):
            if user == 'Clem' or user == 'A member':
                return '/membres/voir/{}/'.format(user)

        md = markdown.Markdown(extensions=[PingExtension(ping_url=ping_url)])
        text = 'I want to ping @Clem, @[Zozor] and @[A member].'
        self.assertEqual(
                '<p>I want to ping <a class="ping" href="/membres/voir/Clem/">@Clem</a>, '
                '@[Zozor] and <a class="ping" href="/membres/voir/A member/">@A member</a>.</p>',
                md.convert(text)
        )
        self.assertEqual({"Clem", "A member"}, md.metadata["ping"])

    def testPingNotMatched(self):
        """ Don't ping when we don't have a space before @ """

        def ping_url(user=None):
            if user == 'Clem' or user == 'A member':
                return '/membres/voir/{}/'.format(user)

        md = markdown.Markdown(extensions=[PingExtension(ping_url=ping_url)])
        text = 'I want to@Clem, @[Zozor] and@[A member].'
        self.assertEqual('<p>' + text + '</p>', md.convert(text))
        self.assertEqual(set(), md.metadata["ping"])
