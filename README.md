Python-ZMarkdown
=================

[![Build Status](http://img.shields.io/travis/zestedesavoir/Python-ZMarkdown.svg)](https://travis-ci.org/zestedesavoir/Python-ZMarkdown)
[![BSD License](http://img.shields.io/badge/license-BSD-yellow.svg)](http://opensource.org/licenses/BSD-3-Clause)

About
-----

This is a small fork of [Python-Markdown](http://packages.python.org/Markdown/) including somes improvements suitables for zds. 

Modification
------------

Main modifications :
- A `master-zds` branch with all modification (`master` will remain updated with upstream)
- Add range support in codehilite's `hl_lines` option
- Add `linenostart` option in codehilite to defining the starting number.

Original Readme
---------------

This is a Python implementation of John Gruber's [Markdown][]. 
It is almost completely compliant with the reference implementation,
though there are a few known issues. See [Features][] for information 
on what exactly is supported and what is not. Additional features are 
supported by the [Available Extensions][].

[Python-Markdown]: http://packages.python.org/Markdown/
[Markdown]: http://daringfireball.net/projects/markdown/
[Features]: http://packages.python.org/Markdown/index.html#Features
[Available Extensions]: http://packages.python.org/Markdown/extensions/index.html


Documentation
-------------

Installation and usage documentation is available in the `docs/` directory
of the distribution and on the project website at 
<http://packages.python.org/Markdown/>.

Support
-------

You may ask for help and discuss various other issues on the [mailing list][] and report bugs on the [bug tracker][].

[mailing list]: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
[bug tracker]: http://github.com/waylan/Python-Markdown/issues 
