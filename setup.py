#!/usr/bin/env python

from __future__ import with_statement
import os
from distutils.core import setup
import imp


def get_version():
    " Get version & version_info without importing markdown.__init__ "
    path = os.path.join(os.path.dirname(__file__), 'markdown')
    fp, pathname, desc = imp.find_module('__version__', [path])
    try:
        v = imp.load_module('__version__', fp, pathname, desc)
        return v.version, v.version_info
    finally:
        fp.close()


version, version_info = get_version()

# Get development Status for classifiers
dev_status_map = {
    'alpha': '3 - Alpha',
    'beta': '4 - Beta',
    'rc': '4 - Beta',
    'final': '5 - Production/Stable',
    'zds': '5 - Production/Stable'
}

if version_info[3] == 'alpha' and version_info[4] == 0:
    DEVSTATUS = '2 - Pre-Alpha'
else:
    DEVSTATUS = dev_status_map[version_info[3]]

long_description = '''
This is a Python implementation of John Gruber's Markdown_.
It is almost completely compliant with the reference implementation,
though there are a few known issues. See Features_ for information
on what exactly is supported and what is not. Additional features are
supported by the `Available Extensions`_.

.. _Markdown: http://daringfireball.net/projects/markdown/
.. _Features: https://pythonhosted.org/Markdown/index.html#Features
.. _`Available Extensions`: https://pythonhosted.org/Markdown/extensions/index.html

Support
=======

You may ask for help and discuss various other issues on the
`mailing list`_ and report bugs on the `bug tracker`_.

.. _`mailing list`: http://lists.sourceforge.net/lists/listinfo/python-markdown-discuss
.. _`bug tracker`: http://github.com/waylan/Python-Markdown/issues
'''

setup(name='Markdown',
      version=version,
      url='https://pythonhosted.org/Markdown/',
      download_url='http://pypi.python.org/packages/source/M/Markdown/Markdown-%s.tar.gz' % version,
      description='Python implementation of Markdown.',
      long_description=long_description,
      author='Manfred Stienstra, Yuri takhteyev and Waylan limberg',
      author_email='waylan.limberg [at] icloud.com',
      maintainer='Waylan Limberg',
      maintainer_email='waylan.limberg [at] icloud.com',
      license='BSD License',
      packages=['markdown', 'markdown.extensions'],
      classifiers=['Development Status :: %s' % DEVSTATUS,
                   'License :: OSI Approved :: BSD License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 2.7',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 3.2',
                   'Programming Language :: Python :: 3.3',
                   'Programming Language :: Python :: 3.4',
                   'Topic :: Communications :: Email :: Filters',
                   'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
                   'Topic :: Internet :: WWW/HTTP :: Site Management',
                   'Topic :: Software Development :: Documentation',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   'Topic :: Text Processing :: Filters',
                   'Topic :: Text Processing :: Markup :: HTML'
                   ]
      )
