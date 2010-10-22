#!/usr/bin/env python
from setuptools import setup, find_packages

VERSION = 0.1

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

KEYWORDS = 'paypal api x adaptive paiements accounts'

setup(name = 'paypalx',
    version = VERSION,
    description = 'Paypal X API implementation in Python.',
    long_description = """An implementation of Paypal X's API in Python. Featuring
    Adaptive API""",
    author = 'Timothee Peignier',
    author_email = 'timothee.peignier@e-loue.com',
    url = 'http://github.com/eloue/python-paypalx',
    packages = find_packages(),
    download_url = 'http://pypi.python.org/pypi/paypal/',
    install_requires = ['distribute', 'httplib2>=0.6.0', 'simplejson>=2.0.9'],
    classifiers = CLASSIFIERS,
    keywords = KEYWORDS,
    zip_safe = True,
    tests_require=['nose', 'coverage'],
    test_suite = "nose.collector"
)
