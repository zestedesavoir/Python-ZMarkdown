"""
Python-Markdown Extension Regression Tests
==========================================

A collection of regression tests to confirm that the included extensions
continue to work as advertised. This used to be accomplished by doctests.

"""

from __future__ import unicode_literals
import unittest
import markdown


class TestExtensionClass(unittest.TestCase):
    """ Test markdown.extensions.Extension. """

    def setUp(self):
        class TestExtension(markdown.extensions.Extension):
            config = {
                'foo': ['bar', 'Description of foo'],
                'bar': ['baz', 'Description of bar']
            }

        self.ext = TestExtension()
        self.ExtKlass = TestExtension

    def testGetConfig(self):
        self.assertEqual(self.ext.getConfig('foo'), 'bar')

    def testGetConfigDefault(self):
        self.assertEqual(self.ext.getConfig('baz'), '')
        self.assertEqual(self.ext.getConfig('baz', default='missing'), 'missing')

    def testGetConfigs(self):
        self.assertEqual(self.ext.getConfigs(), {'foo': 'bar', 'bar': 'baz'})

    def testGetConfigInfo(self):
        self.assertEqual(
            dict(self.ext.getConfigInfo()),
            dict([
                ('foo', 'Description of foo'),
                ('bar', 'Description of bar')
            ])
        )

    def testSetConfig(self):
        self.ext.setConfig('foo', 'baz')
        self.assertEqual(self.ext.getConfigs(), {'foo': 'baz', 'bar': 'baz'})

    def testSetConfigWithBadKey(self):
        # self.ext.setConfig('bad', 'baz) ==> KeyError
        self.assertRaises(KeyError, self.ext.setConfig, 'bad', 'baz')

    def testConfigAsKwargsOnInit(self):
        ext = self.ExtKlass(foo='baz', bar='blah')
        self.assertEqual(ext.getConfigs(), {'foo': 'baz', 'bar': 'blah'})


class TestAbbr(unittest.TestCase):
    """ Test abbr extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['markdown.extensions.abbr'])

    def testSimpleAbbr(self):
        """ Test Abbreviations. """
        text = 'Some text with an ABBR and a REF. Ignore REFERENCE and ref.' + \
               '\n\n*[ABBR]: Abbreviation\n' + \
               '*[REF]: Abbreviation Reference'
        self.assertEqual(
            self.md.convert(text),
            '<p>Some text with an <abbr title="Abbreviation">ABBR</abbr> '
            'and a <abbr title="Abbreviation Reference">REF</abbr>. Ignore '
            'REFERENCE and ref.</p>'
        )

    def testNestedAbbr(self):
        """ Test Nested Abbreviations. """
        text = '[ABBR](/foo) and _ABBR_\n\n' + \
               '*[ABBR]: Abreviation'
        self.assertEqual(
            self.md.convert(text),
            '<p><a href="/foo"><abbr title="Abreviation">ABBR</abbr></a> '
            'and <em><abbr title="Abreviation">ABBR</abbr></em></p>'
        )


class TestCodeHilite(unittest.TestCase):
    """ Test codehilite extension. """

    def setUp(self):
        self.has_pygments = True
        try:
            import pygments  # noqa
        except ImportError:
            self.has_pygments = False

    def testBasicCodeHilite(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(extensions=['markdown.extensions.codehilite'])
        if self.has_pygments:
            # Pygments can use random lexer here as we did not specify the language
            self.assertTrue(md.convert(text).startswith('<div class="codehilite"><pre>'))
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsTrue(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=True)])
        if self.has_pygments:
            # Different versions of pygments output slightly different markup.
            # So we use 'startwith' and test just enough to confirm that
            # pygments received and processed linenums.
            self.assertTrue(
                md.convert(text).startswith(
                    '<table class="codehilitetable"><tr><td class="linenos">'
                )
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="linenums"># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsFalse(self):
        text = '\t#!Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=False)])
        if self.has_pygments:
            self.assertEqual(
                md.convert(text),
                '<div class="codehilite"><pre>'
                '<span></span>'
                '<span class="c1"># A Code Comment</span>\n'
                '</pre></div>'
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-python"># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsNone(self):
        text = '\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=None)])
        if self.has_pygments:
            # Pygments can use random lexer here as we did not specify the language
            self.assertTrue(md.convert(text).startswith('<div class="codehilite"><pre>'))
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsNoneWithShebang(self):
        text = '\t#!Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=None)])
        if self.has_pygments:
            # Differant versions of pygments output slightly different markup.
            # So we use 'startwith' and test just enough to confirm that
            # pygments received and processed linenums.
            self.assertTrue(
                md.convert(text).startswith(
                    '<table class="codehilitetable"><tr><td class="linenos">'
                )
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-python linenums"># A Code Comment'
                '</code></pre>'
            )

    def testLinenumsNoneWithColon(self):
        text = '\t:::Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(linenums=None)]
        )
        if self.has_pygments:
            self.assertEqual(
                md.convert(text),
                '<div class="codehilite"><pre>'
                '<span></span>'
                '<span class="c1"># A Code Comment</span>\n'
                '</pre></div>'
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<pre class="codehilite"><code class="language-python"># A Code Comment'
                '</code></pre>'
            )

    def testHighlightLinesWithColon(self):
        # Test with hl_lines delimited by single or double quotes.
        text0 = '\t:::Python hl_lines="2"\n\t#line 1\n\t#line 2\n\t#line 3'
        text1 = "\t:::Python hl_lines='2'\n\t#line 1\n\t#line 2\n\t#line 3"

        for text in (text0, text1):
            md = markdown.Markdown(extensions=['markdown.extensions.codehilite'])
            if self.has_pygments:
                self.assertEqual(
                    md.convert(text),
                    '<div class="codehilite"><pre>'
                    '<span></span>'
                    '<span class="c1">#line 1</span>\n'
                    '<span class="hll"><span class="c1">#line 2</span>\n</span>'
                    '<span class="c1">#line 3</span>\n'
                    '</pre></div>'
                )
            else:
                self.assertEqual(
                    md.convert(text),
                    '<pre class="codehilite">'
                    '<code class="language-python">#line 1\n'
                    '#line 2\n'
                    '#line 3</code></pre>'
                )

    def testUsePygmentsFalse(self):
        text = '\t:::Python\n\t# A Code Comment'
        md = markdown.Markdown(
            extensions=[markdown.extensions.codehilite.CodeHiliteExtension(use_pygments=False)]
        )
        self.assertEqual(
            md.convert(text),
            '<pre class="codehilite"><code class="language-python"># A Code Comment'
            '</code></pre>'
        )


class TestFencedCode(unittest.TestCase):
    """ Test fenced_code extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['markdown.extensions.fenced_code'])
        self.has_pygments = True
        try:
            import pygments  # noqa
        except ImportError:
            self.has_pygments = False

    def testBasicFence(self):
        """ Test Fenced Code Blocks. """
        text = '''
A paragraph before a fenced code block:

~~~
Fenced code block
~~~'''
        print("-"*20)
        print(self.md.convert(text))
        print("-"*20)
        self.assertEqual(
            self.md.convert(text),
            '<p>A paragraph before a fenced code block:</p>\n'
            '<div><pre><code>Fenced code block\n'
            '</code></pre></div>'
        )

    def testNestedFence(self):
        """ Test nested fence. """

        text = '''
~~~~~~~~

~~~~
~~~~~~~~'''
        self.assertEqual(
            self.md.convert(text),
            '<div><pre><code>\n\n'
            '~~~~\n'
            '</code></pre></div>'
        )

    def testFencedLanguage(self):
        """ Test Language Tags. """

        text = '''
~~~~{.python}
# Some python code
~~~~'''
        self.assertEqual(
            self.md.convert(text),
            '<div><pre><code class="python"># Some python code\n'
            '</code></pre></div>'
        )

    def testFencedBackticks(self):
        """ Test Code Fenced with Backticks. """

        text = '''
`````
# Arbitrary code
~~~~~ # these tildes will not close the block
`````'''
        self.assertEqual(
            self.md.convert(text),
            '<div><pre><code># Arbitrary code\n'
            '~~~~~ # these tildes will not close the block\n'
            '</code></pre></div>'
        )

    def testFencedCodeWithHighlightLines(self):
        """ Test Fenced Code with Highlighted Lines. """

        text = '''
```hl_lines="1 3"
line 1
line 2
line 3
```'''
        md = markdown.Markdown(
            extensions=[
                markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                'markdown.extensions.fenced_code'
            ]
        )

        if self.has_pygments:
            self.assertEqual(
                md.convert(text),
                '<div><div class="codehilite"><pre>'
                '<span></span>'
                '<span class="hll">line 1\n</span>'
                'line 2\n'
                '<span class="hll">line 3\n</span>'
                '</pre></div>\n</div>'
            )
        else:
            self.assertEqual(
                md.convert(text),
                '<div><pre class="codehilite"><code>line 1\n'
                'line 2\n'
                'line 3</code></pre></div>'
            )

    def testFencedLanguageAndHighlightLines(self):
        """ Test Fenced Code with Highlighted Lines. """

        text0 = '''
```.python hl_lines="1 3"
#line 1
#line 2
#line 3
```'''
        text1 = '''
~~~{.python hl_lines='1 3'}
#line 1
#line 2
#line 3
~~~'''
        for text in (text0, text1):
            md = markdown.Markdown(
                extensions=[
                    markdown.extensions.codehilite.CodeHiliteExtension(linenums=None, guess_lang=False),
                    'markdown.extensions.fenced_code'
                ]
            )
            if self.has_pygments:
                self.assertEqual(
                    md.convert(text),
                    '<div><div class="codehilite"><pre>'
                    '<span></span>'
                    '<span class="hll"><span class="c1">#line 1</span>\n</span>'
                    '<span class="c1">#line 2</span>\n'
                    '<span class="hll"><span class="c1">#line 3</span>\n</span>'
                    '</pre></div>\n</div>'
                )
            else:
                self.assertEqual(
                    md.convert(text),
                    '<div><pre class="codehilite"><code class="language-python">#line 1\n'
                    '#line 2\n'
                    '#line 3</code></pre>\n</div>'
                )
