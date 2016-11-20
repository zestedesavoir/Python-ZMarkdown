# -*- encoding: utf-8 -*-
from __future__ import unicode_literals
import unittest
import markdown
from markdown.extensions.header_dec import DownHeaderExtension
from markdown.extensions.zds import ZdsExtension
from markdown.extensions.ping import PingExtension
from markdown.extensions.french_typography import FrenchTypographyExtension
from markdown.extensions.title_anchor import TitleAnchorExtension


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
                '<p>&gt;&#x202F;![Image](http://test.com/image.png)\n</p>')

    def test_ping_function(self):
        def ping_url(user=None):
            if user == 'Clem':
                return '/membres/voir/{}/'.format(user)

        zds_ext = ZdsExtension(ping_url=ping_url)
        md = markdown.Markdown(extensions=[zds_ext])
        text = 'I want to ping @[Clem] and @[Zozor].'
        self.assertEqual(
                '<p>I want to ping <a class="ping" href="/membres/voir/Clem/">@Clem</a> and @[Zozor].</p>',
                md.convert(text)
        )
        self.assertEqual({"Clem"}, md.metadata["ping"])

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
                '<h2>Title 2b</h2>')
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
                '<h3>Title 2b</h3>')
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
                '<h4>Title 2b</h4>')

    def test_typography(self):
        zds_ext = ZdsExtension(emoticons={":D": "image.png"})
        md = markdown.Markdown(extensions=[zds_ext])

        self.assertEqual(
                """<p>Petit &laquo;&nbsp;essai&nbsp;&raquo; un peu plus <code>&lt;&lt; complet 'sur la typo' &gt;"""
                """&gt;</code>&#x202F;!</p>\n"""
                """<div><table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1</pre>"""
                """</div></td><td class="code"><div class="codehilite"><pre><span></span>Petit &lt;&lt; essai &gt;"""
                """&gt; un peu plus `&lt;&lt; complet &#39;sur la typo&#39; &gt;&gt; !\n"""
                """</pre></div>\n"""
                """</td></tr></table></div>\n"""
                """<div><table class="codehilitetable"><tr><td class="linenos"><div class="linenodiv"><pre>1\n"""
                """2</pre></div></td><td class="code"><div class="codehilite"><pre><span></span><span class="n">a<"""
                """/span> <span class="o">=</span> <span class="mi">42</span> <span class="o">&gt;&gt;"""
                """</span> <span class="mi">2</span>\n"""
                """<span class="n">b</span> <span class="o">=</span> <span class="s1">&#39;zds&#39;</span>\n"""
                """</pre></div>\n"""
                """</td></tr></table></div>""",

                md.convert("Petit << essai >> un peu plus `<< complet 'sur la typo' >>` !\n\n"
                           "```\n"
                           "Petit << essai >> un peu plus `<< complet 'sur la typo' >> !\n"
                           "```\n\n"
                           "```python\n"
                           "a = 42 >> 2\n"
                           "b = 'zds'\n"
                           "```\n"))


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


class TestTypography(unittest.TestCase):
    def setUp(self):
        self.md = markdown.Markdown(extensions=[FrenchTypographyExtension()])

    def simple_comparison(self, src, result):
        self.assertEqual(
                '<p>{}</p>'.format(result),
                self.md.convert(src))

    def test_basic(self):
        self.simple_comparison("c'est", "c&rsquo;est")
        self.simple_comparison("un --- deux", "un &mdash; deux")
        self.simple_comparison("un -- deux", "un &ndash; deux")
        self.simple_comparison("un ; deux", "un&#x202F;; deux")
        self.simple_comparison("un : deux", "un&#x202F;: deux")
        self.simple_comparison("un ? deux", "un&#x202F;? deux")
        self.simple_comparison("un ??? deux", "un&#x202F;??? deux")
        self.simple_comparison("un ! deux", "un&#x202F;! deux")
        self.simple_comparison("un !!! deux", "un&#x202F;!!! deux")
        self.simple_comparison("42 %", "42&nbsp;%")
        self.simple_comparison("42 ‰", "42&nbsp;&permil;")
        self.simple_comparison("« Zeste »", "&laquo;&nbsp;Zeste&nbsp;&raquo;")
        self.simple_comparison("<<Zeste>>", "&laquo;Zeste&raquo;")
        self.simple_comparison("<< Zeste >>", "&laquo;&nbsp;Zeste&nbsp;&raquo;")
        self.simple_comparison("42%o", "42&permil;")
        self.simple_comparison("42 %o", "42&nbsp;&permil;")
        self.simple_comparison("42...", "42&hellip;")

    def test_escape(self):
        self.simple_comparison(r"c\'est", "c'est")
        self.simple_comparison(r"un \-\-- deux", "un --- deux")
        self.simple_comparison(r"un \-- deux", "un -- deux")
        self.simple_comparison(r"un\ ; deux", "un ; deux")
        self.simple_comparison(r"un\ : deux", "un : deux")
        self.simple_comparison(r"un\ ? deux", "un ? deux")
        self.simple_comparison(r"un\ ! deux", "un ! deux")
        self.simple_comparison(r"42\ %", "42 %")
        self.simple_comparison(r"42\ ‰", "42 ‰")
        self.simple_comparison(r"\« Zeste\ »", "« Zeste »")
        self.simple_comparison(r"\<<Zeste\>>", "&lt;&lt;Zeste&gt;&gt;")
        self.simple_comparison(r"\<< Zeste\ \>>", "&lt;&lt; Zeste &gt;&gt;")
        self.simple_comparison(r"42\%o", "42%o")
        self.simple_comparison(r"42 \%o", "42 %o")
        self.simple_comparison(r"42\...", "42...")

    def test_neg(self):
        self.simple_comparison("un - deux", "un - deux")
        self.simple_comparison("un ---- deux", "un ---- deux")
        self.simple_comparison("un ;) deux", "un ;) deux")
        self.simple_comparison("un :) deux", "un :) deux")
        self.simple_comparison(r"< < Zeste > >", "&lt; &lt; Zeste &gt; &gt;")


class TestTitleAnchor(unittest.TestCase):
    def test_title_anchor(self):
        text_ref = ('# Title 1\n'
                    'a\n'
                    '## Title 2\n'
                    'b\n'
                    '### Title 3\n'
                    'c\n'
                    '#### Title 4\n'
                    'd\n'
                    '##### Title 5-1\n'
                    'e\n'
                    '##### Title 5\n'
                    'f\n'
                    '##### Title 5\n'
                    'g\n'
                    '###### Title 6\n'
                    'h\n'
                    '###### Title 6-1\n'
                    'i\n\n'
                    'Title 1b\n'
                    '========\n'
                    'j\n\n'
                    'Title 2b\n'
                    '--------\n\n'
                    'k\n'
                    "> # Title 1\n\n"
                    'l\n')

        md = markdown.Markdown(extensions=[])
        self.assertEqual(
                md.convert(text_ref),
                '<h1>Title 1</h1>\n'
                '<p>a</p>\n'
                '<h2>Title 2</h2>\n'
                '<p>b</p>\n'
                '<h3>Title 3</h3>\n'
                '<p>c</p>\n'
                '<h4>Title 4</h4>\n'
                '<p>d</p>\n'
                '<h5>Title 5-1</h5>\n'
                '<p>e</p>\n'
                '<h5>Title 5</h5>\n'
                '<p>f</p>\n'
                '<h5>Title 5</h5>\n'
                '<p>g</p>\n'
                '<h6>Title 6</h6>\n'
                '<p>h</p>\n'
                '<h6>Title 6-1</h6>\n'
                '<p>i</p>\n'
                '<h1>Title 1b</h1>\n'
                '<p>j</p>\n'
                '<h2>Title 2b</h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1>Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

        md = markdown.Markdown(extensions=[TitleAnchorExtension()])
        self.assertEqual(
                md.convert(text_ref),
                '<h1 id="title-1">Title 1</h1>\n'
                '<p>a</p>\n'
                '<h2 id="title-2">Title 2</h2>\n'
                '<p>b</p>\n'
                '<h3 id="title-3">Title 3</h3>\n'
                '<p>c</p>\n'
                '<h4 id="title-4">Title 4</h4>\n'
                '<p>d</p>\n'
                '<h5 id="title-5-1">Title 5-1</h5>\n'
                '<p>e</p>\n'
                '<h5 id="title-5">Title 5</h5>\n'
                '<p>f</p>\n'
                '<h5 id="title-5-2">Title 5</h5>\n'
                '<p>g</p>\n'
                '<h6 id="title-6">Title 6</h6>\n'
                '<p>h</p>\n'
                '<h6 id="title-6-1">Title 6-1</h6>\n'
                '<p>i</p>\n'
                '<h1 id="title-1b">Title 1b</h1>\n'
                '<p>j</p>\n'
                '<h2 id="title-2b">Title 2b</h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1>Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

        md = markdown.Markdown(extensions=[TitleAnchorExtension(root_only=False)])
        self.assertEqual(
                md.convert(text_ref),
                '<h1 id="title-1">Title 1</h1>\n'
                '<p>a</p>\n'
                '<h2 id="title-2">Title 2</h2>\n'
                '<p>b</p>\n'
                '<h3 id="title-3">Title 3</h3>\n'
                '<p>c</p>\n'
                '<h4 id="title-4">Title 4</h4>\n'
                '<p>d</p>\n'
                '<h5 id="title-5-1">Title 5-1</h5>\n'
                '<p>e</p>\n'
                '<h5 id="title-5">Title 5</h5>\n'
                '<p>f</p>\n'
                '<h5 id="title-5-2">Title 5</h5>\n'
                '<p>g</p>\n'
                '<h6 id="title-6">Title 6</h6>\n'
                '<p>h</p>\n'
                '<h6 id="title-6-1">Title 6-1</h6>\n'
                '<p>i</p>\n'
                '<h1 id="title-1b">Title 1b</h1>\n'
                '<p>j</p>\n'
                '<h2 id="title-2b">Title 2b</h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1 id="title-1-1">Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

        md = markdown.Markdown(extensions=[TitleAnchorExtension(starting_title=2, ending_title=5)])
        self.assertEqual(
                md.convert(text_ref),
                '<h1>Title 1</h1>\n'
                '<p>a</p>\n'
                '<h2 id="title-2">Title 2</h2>\n'
                '<p>b</p>\n'
                '<h3 id="title-3">Title 3</h3>\n'
                '<p>c</p>\n'
                '<h4 id="title-4">Title 4</h4>\n'
                '<p>d</p>\n'
                '<h5 id="title-5-1">Title 5-1</h5>\n'
                '<p>e</p>\n'
                '<h5 id="title-5">Title 5</h5>\n'
                '<p>f</p>\n'
                '<h5 id="title-5-2">Title 5</h5>\n'
                '<p>g</p>\n'
                '<h6>Title 6</h6>\n'
                '<p>h</p>\n'
                '<h6>Title 6-1</h6>\n'
                '<p>i</p>\n'
                '<h1>Title 1b</h1>\n'
                '<p>j</p>\n'
                '<h2 id="title-2b">Title 2b</h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1>Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

        md = markdown.Markdown(extensions=[TitleAnchorExtension(marker_key="zds")])
        self.assertEqual(
                md.convert(text_ref),
                '<h1 id="zds-title-1">Title 1</h1>\n'
                '<p>a</p>\n'
                '<h2 id="zds-title-2">Title 2</h2>\n'
                '<p>b</p>\n'
                '<h3 id="zds-title-3">Title 3</h3>\n'
                '<p>c</p>\n'
                '<h4 id="zds-title-4">Title 4</h4>\n'
                '<p>d</p>\n'
                '<h5 id="zds-title-5-1">Title 5-1</h5>\n'
                '<p>e</p>\n'
                '<h5 id="zds-title-5">Title 5</h5>\n'
                '<p>f</p>\n'
                '<h5 id="zds-title-5-2">Title 5</h5>\n'
                '<p>g</p>\n'
                '<h6 id="zds-title-6">Title 6</h6>\n'
                '<p>h</p>\n'
                '<h6 id="zds-title-6-1">Title 6-1</h6>\n'
                '<p>i</p>\n'
                '<h1 id="zds-title-1b">Title 1b</h1>\n'
                '<p>j</p>\n'
                '<h2 id="zds-title-2b">Title 2b</h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1>Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

        md = markdown.Markdown(extensions=[TitleAnchorExtension(link_position="before")])
        self.assertEqual(
                md.convert(text_ref),
                '<h1 id="title-1"><a href="#title-1"><span class="anchor-link"></span></a>Title 1</h1>\n'
                '<p>a</p>\n'
                '<h2 id="title-2"><a href="#title-2"><span class="anchor-link"></span></a>Title 2</h2>\n'
                '<p>b</p>\n'
                '<h3 id="title-3"><a href="#title-3"><span class="anchor-link"></span></a>Title 3</h3>\n'
                '<p>c</p>\n'
                '<h4 id="title-4"><a href="#title-4"><span class="anchor-link"></span></a>Title 4</h4>\n'
                '<p>d</p>\n'
                '<h5 id="title-5-1"><a href="#title-5-1"><span class="anchor-link"></span></a>Title 5-1</h5>\n'
                '<p>e</p>\n'
                '<h5 id="title-5"><a href="#title-5"><span class="anchor-link"></span></a>Title 5</h5>\n'
                '<p>f</p>\n'
                '<h5 id="title-5-2"><a href="#title-5-2"><span class="anchor-link"></span></a>Title 5</h5>\n'
                '<p>g</p>\n'
                '<h6 id="title-6"><a href="#title-6"><span class="anchor-link"></span></a>Title 6</h6>\n'
                '<p>h</p>\n'
                '<h6 id="title-6-1"><a href="#title-6-1"><span class="anchor-link"></span></a>Title 6-1</h6>\n'
                '<p>i</p>\n'
                '<h1 id="title-1b"><a href="#title-1b"><span class="anchor-link"></span></a>Title 1b</h1>\n'
                '<p>j</p>\n'
                '<h2 id="title-2b"><a href="#title-2b"><span class="anchor-link"></span></a>Title 2b</h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1>Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

        md = markdown.Markdown(extensions=[TitleAnchorExtension(link_position="after")])
        self.assertEqual(
                md.convert(text_ref),
                '<h1 id="title-1">Title 1<a href="#title-1"><span class="anchor-link"></span></a></h1>\n'
                '<p>a</p>\n'
                '<h2 id="title-2">Title 2<a href="#title-2"><span class="anchor-link"></span></a></h2>\n'
                '<p>b</p>\n'
                '<h3 id="title-3">Title 3<a href="#title-3"><span class="anchor-link"></span></a></h3>\n'
                '<p>c</p>\n'
                '<h4 id="title-4">Title 4<a href="#title-4"><span class="anchor-link"></span></a></h4>\n'
                '<p>d</p>\n'
                '<h5 id="title-5-1">Title 5-1<a href="#title-5-1"><span class="anchor-link"></span></a></h5>\n'
                '<p>e</p>\n'
                '<h5 id="title-5">Title 5<a href="#title-5"><span class="anchor-link"></span></a></h5>\n'
                '<p>f</p>\n'
                '<h5 id="title-5-2">Title 5<a href="#title-5-2"><span class="anchor-link"></span></a></h5>\n'
                '<p>g</p>\n'
                '<h6 id="title-6">Title 6<a href="#title-6"><span class="anchor-link"></span></a></h6>\n'
                '<p>h</p>\n'
                '<h6 id="title-6-1">Title 6-1<a href="#title-6-1"><span class="anchor-link"></span></a></h6>\n'
                '<p>i</p>\n'
                '<h1 id="title-1b">Title 1b<a href="#title-1b"><span class="anchor-link"></span></a></h1>\n'
                '<p>j</p>\n'
                '<h2 id="title-2b">Title 2b<a href="#title-2b"><span class="anchor-link"></span></a></h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1>Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

    def test_toc(self):
        text_ref = ('# Title 1\n'
                    'a\n'
                    '## Title 2\n'
                    'b\n'
                    '### Title 3\n'
                    'c\n'
                    '#### Title 4\n'
                    'd\n'
                    '##### Title 5-1\n'
                    'e\n'
                    '##### Title 5\n'
                    'f\n'
                    '##### Title 5\n'
                    'g\n'
                    '###### Title 6\n'
                    'h\n'
                    '###### Title 6-1\n'
                    'i\n\n'
                    'Title 1b\n'
                    '========\n'
                    'j\n\n'
                    'Title 2b\n'
                    '--------\n\n'
                    'k\n'
                    "> # Title 1\n\n"
                    'l\n')
        md = markdown.Markdown(extensions=[TitleAnchorExtension(marker_key="zds", link_position="before")])
        self.assertEqual(
                md.convert(text_ref),
                '<h1 id="zds-title-1"><a href="#zds-title-1"><span class="anchor-link"></span></a>Title 1</h1>\n'
                '<p>a</p>\n'
                '<h2 id="zds-title-2"><a href="#zds-title-2"><span class="anchor-link"></span></a>Title 2</h2>\n'
                '<p>b</p>\n'
                '<h3 id="zds-title-3"><a href="#zds-title-3"><span class="anchor-link"></span></a>Title 3</h3>\n'
                '<p>c</p>\n'
                '<h4 id="zds-title-4"><a href="#zds-title-4"><span class="anchor-link"></span></a>Title 4</h4>\n'
                '<p>d</p>\n'
                '<h5 id="zds-title-5-1"><a href="#zds-title-5-1"><span class="anchor-link"></span></a>Title 5-1</h5>\n'
                '<p>e</p>\n'
                '<h5 id="zds-title-5"><a href="#zds-title-5"><span class="anchor-link"></span></a>Title 5</h5>\n'
                '<p>f</p>\n'
                '<h5 id="zds-title-5-2"><a href="#zds-title-5-2"><span class="anchor-link"></span></a>Title 5</h5>\n'
                '<p>g</p>\n'
                '<h6 id="zds-title-6"><a href="#zds-title-6"><span class="anchor-link"></span></a>Title 6</h6>\n'
                '<p>h</p>\n'
                '<h6 id="zds-title-6-1"><a href="#zds-title-6-1"><span class="anchor-link"></span></a>Title 6-1</h6>\n'
                '<p>i</p>\n'
                '<h1 id="zds-title-1b"><a href="#zds-title-1b"><span class="anchor-link"></span></a>Title 1b</h1>\n'
                '<p>j</p>\n'
                '<h2 id="zds-title-2b"><a href="#zds-title-2b"><span class="anchor-link"></span></a>Title 2b</h2>\n'
                '<p>k</p>\n'
                '<blockquote>\n'
                '<h1>Title 1</h1>\n'
                '</blockquote>\n'
                '<p>l</p>')

        toc = md.metadata.get("toc", None)
        self.assertIsNotNone(toc)
        self.assertEqual(11, len(toc))

        self.assertEqual("Title 1", toc[0].title)
        self.assertEqual("zds-title-1", toc[0].anchor)
        self.assertEqual(1, toc[0].level)

        self.assertEqual("Title 2", toc[1].title)
        self.assertEqual("zds-title-2", toc[1].anchor)
        self.assertEqual(2, toc[1].level)

        self.assertEqual("Title 3", toc[2].title)
        self.assertEqual("zds-title-3", toc[2].anchor)
        self.assertEqual(3, toc[2].level)

        self.assertEqual("Title 4", toc[3].title)
        self.assertEqual("zds-title-4", toc[3].anchor)
        self.assertEqual(4, toc[3].level)

        self.assertEqual("Title 5-1", toc[4].title)
        self.assertEqual("zds-title-5-1", toc[4].anchor)
        self.assertEqual(5, toc[4].level)

        self.assertEqual("Title 5", toc[5].title)
        self.assertEqual("zds-title-5", toc[5].anchor)
        self.assertEqual(5, toc[5].level)

        self.assertEqual("Title 5", toc[6].title)
        self.assertEqual("zds-title-5-2", toc[6].anchor)
        self.assertEqual(5, toc[6].level)

        self.assertEqual("Title 6", toc[7].title)
        self.assertEqual("zds-title-6", toc[7].anchor)
        self.assertEqual(6, toc[7].level)

        self.assertEqual("Title 6-1", toc[8].title)
        self.assertEqual("zds-title-6-1", toc[8].anchor)
        self.assertEqual(6, toc[8].level)

        self.assertEqual("Title 1b", toc[9].title)
        self.assertEqual("zds-title-1b", toc[9].anchor)
        self.assertEqual(1, toc[9].level)

        self.assertEqual("Title 2b", toc[10].title)
        self.assertEqual("zds-title-2b", toc[10].anchor)
        self.assertEqual(2, toc[10].level)
