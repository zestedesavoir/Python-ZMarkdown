#!/usr/bin/env python

from __future__ import with_statement
import os
from distutils.core import setup
import imp


def get_version():
    " Get version & version_info without importing markdown.__init__ "
    path = os.path.join(os.path.dirname(__file__), 'zmarkdown')
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
}

if version_info[3] == 'alpha' and version_info[4] == 0:
    DEVSTATUS = '2 - Pre-Alpha'
else:
    DEVSTATUS = dev_status_map[version_info[3]]

long_description = '''
Small fork of Python-Markdown suitable for zestedesavoir.com needs
'''

setup(name='Markdown',
      version=version,
      url='https://github.com/zestedesavoir/Python-ZMarkdown',
      description='Python implementation of Markdown.',
      long_description=long_description,
      author='Manfred Stienstra, Yuri takhteyev, Waylan limberg and zeste de savoir members',
      author_email='christophe.gabard [at] gmail.com',
      maintainer='Christophe Gabard',
      maintainer_email='christophe.gabard [at] gmail.com',
      license='BSD License',
      packages=['zmarkdown', 'zmarkdown.extensions'],
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
