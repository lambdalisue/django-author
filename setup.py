#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Alisue
# Last Change:  18-Mar-2011.
#
import sys
import os
from setuptools import setup, find_packages

version = "0.2.0"

# Make sure the django.mo file also exists:
if 'sdist' in sys.argv:
    try:
        os.chdir('author')
        from django.core.management.commands.compilemessages import compile_messages
        compile_messages(sys.stderr)
    finally:
        os.chdir('..')

def read(filename):
    import os.path
    return open(os.path.join(os.path.dirname(__file__), filename)).read()

setup(
    name="django-author",
    version=version,
    description = "Add special User ForeignKey fields which update automatically",
    long_description=read('README.rst'),
    classifiers = [
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    keywords = "django author object universal",
    author = "Alisue",
    author_email = "lambdalisue@hashnote.net",
    url=r"https://github.com/lambdalisue/django-author",
    download_url = r"https://github.com/lambdalisue/django-author/tarball/master",
    license = 'MIT',
    packages = find_packages(),
    include_package_data = True,
    zip_safe = True,
    install_requires=[
        'distribute',
        'setuptools-git',
        ],
    test_suite = 'tests.runtests.runtests',
)
