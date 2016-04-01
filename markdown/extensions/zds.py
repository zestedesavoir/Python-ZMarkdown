from __future__ import absolute_import
from __future__ import unicode_literals
from . import Extension

from .abbr import AbbrExtension
from .align import AlignExtension
from .codehilite import CodeHiliteExtension
from .comments import CommentsExtension
from .customblock import CustomBlockExtension
from .delext import DelExtension
from .emoticons import EmoticonExtension
from .fenced_code import FencedCodeExtension
from .footnotes import FootnoteExtension
from .grid_tables import GridTableExtension
from .header_dec import DownHeaderExtension
from .kbd import KbdExtension
from .mathjax import MathJaxExtension
from .ping import PingExtension
from .smart_legend import SmartLegendExtension
from .smarty import SmartyExtension
from .subsuperscript import SubSuperscriptExtension
from .tables import TableExtension
from .urlize import UrlizeExtension
from .video import VideoExtension


class ZdsExtension(Extension):
    """ Add various extensions to Markdown class."""

    def __init__(self, *args, **kwargs):
        self.config = {
            'inline': [False, ''],
            'emoticons': [{}, ''],
            'js_support': [False, ''],
            'pings': [[], ''],
        }

        super(ZdsExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md, md_globals):
        """ Register extension instances. """
        self.inline = self.getConfigs().get("inline", True)
        self.emoticons = self.getConfigs().get("emoticons", {})
        self.js_support = self.getConfigs().get("js_support", False)
        md.inline = self.inline

        def is_pinged(user=None):
            return False

        self.is_pinged = self.getConfigs().get('is_pinged', is_pinged)

        # create extensions :
        sub_ext = SubSuperscriptExtension()  # Sub and Superscript support
        del_ext = DelExtension()  # Del support
        urlize_ext = UrlizeExtension()  # Autolink support
        sm_ext = SmartyExtension(smart_quotes=False)
        ping_ext = PingExtension(is_pinged=self.is_pinged)  # Ping support
        # Define used ext
        exts = [sub_ext,  # Subscript support
                del_ext,  # Del support
                urlize_ext,  # Autolink support
                ping_ext,  # Ping support
                sm_ext]

        if not self.inline:
            mathjax_ext = MathJaxExtension()  # MathJax support
            kbd_ext = KbdExtension()  # Keyboard support
            emo_ext = EmoticonExtension(emoticons=self.emoticons)  # smileys support
            customblock_ext = CustomBlockExtension(classes={
                "s(ecret)?": "spoiler",
                "i(nformation)?": "information ico-after",
                "q(uestion)?": "question ico-after",
                "a(ttention)?": "warning ico-after",
                "e(rreur)?": "error ico-after",
            })  # CustomBlock support
            align_ext = AlignExtension()  # Right align and center support
            video_ext = VideoExtension(js_support=self.js_support)  # Video support

            gridtable_ext = GridTableExtension()  # Grid Table support
            comment_ext = CommentsExtension(start_tag="<--COMMENT", end_tag="COMMENT-->")  # Comment support
            legend_ext = SmartLegendExtension()  # Smart Legend support
            dheader_ext = DownHeaderExtension(offset=2)  # Offset header support

            exts.extend([AbbrExtension(),  # Abbreviation support, included in python-markdown
                         FootnoteExtension(),  # Footnotes support, included in python-markdown
                         # Footnotes place marker can be set with the PLACE_MARKER option
                         TableExtension(),  # Tables support, included in python-markdown
                         # Extended syntaxe for code block support, included in python-markdown
                         CodeHiliteExtension(linenums=True, guess_lang=False),
                         customblock_ext,  # CustomBlock support
                         kbd_ext,  # Kbd support
                         emo_ext,  # Smileys support
                         video_ext,  # Video support
                         gridtable_ext,  # Grid tables support
                         align_ext,  # Right align and center support
                         dheader_ext,  # Down Header support
                         mathjax_ext,  # Mathjax support
                         FencedCodeExtension(),
                         comment_ext,  # Comment support
                         legend_ext,  # Legend support
                         ])
        md.registerExtensions(exts, {})
        if self.inline:
            md.inlinePatterns.pop("image_link")
            md.inlinePatterns.pop("image_reference")
            md.inlinePatterns.pop("reference")
            md.inlinePatterns.pop("short_reference")
            md.inlinePatterns.pop("linebreak")


def makeExtension(*args, **kwargs):
    return ZdsExtension(*args, **kwargs)
