# coding: utf-8

import codecs
import markdown
from markdown.extensions.zds import ZdsExtension
import time

# Markdowns customs extensions :
def get_markdown_instance(Inline=False):
    zdsext = ZdsExtension({"inline": Inline, "emoticons": {"TOTOTO":"truc"}, "js_support": True})
    # Generate parser
    md = markdown.Markdown(extensions=(zdsext,),
                           safe_mode = 'escape',
                           # Protect use of html by escape it
                           enable_attributes = False,
                           # Disable the conversion of attributes.
                           # This could potentially allow an
                           # untrusted user to inject JavaScript
                           # into documents.
                           tab_length = 4,
                           # Length of tabs in the source.
                           # This is the default value
                           output_format = 'html5',      # html5 output
                           # This is the default value
                           smart_emphasis = True,
                           # Enable smart emphasis for underscore syntax
                           lazy_ol = True,
                           # Enable smart ordered list start support
                           )
    return md

input_file = codecs.open("prob.md", mode="r", encoding="utf-8")
text = input_file.read()
print(get_markdown_instance(Inline=False).convert(text).encode('utf-8'))

