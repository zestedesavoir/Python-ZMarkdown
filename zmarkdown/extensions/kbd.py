#! /usr/bin/env python

from zmarkdown.extensions import Extension
from zmarkdown.inlinepatterns import SimpleTagPattern

# Small extension to parse ||Touche|| in Kbd html tag

KBD_RE = r"(\|\|)(.+?)(\|\|)"


class KbdExtension(Extension):
    """Adds kdb extension to Markdown class."""

    def extendZMarkdown(self, md, md_globals):
        """Modifies inline patterns."""
        md.inlinePatterns.add('kbd', SimpleTagPattern(KBD_RE, 'kbd'), '<not_strong')


def makeExtension(*args, **kwargs):
    return KbdExtension(*args, **kwargs)
