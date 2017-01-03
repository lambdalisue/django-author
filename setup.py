#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author:       Alisue
# Last Change:  18-Mar-2011.
#
import sys
import os
from setuptools import setup, find_packages, Command
from setuptools.command.sdist import sdist as original_sdist

version = "0.4.5"

class compile_messages(Command):
    description = ("re-compile local message files ('.po' to '.mo'). "
                   "it require django-admin.py")
    user_options = []

    def initialize_options(self):
        self.cwd = None

    def finalize_options(self):
        self.cwd = os.getcwd()

    def run(self):
        compile_messages.compile_messages()

    @classmethod
    def compile_messages(cls):
        """
        Compile '.po' into '.mo' via 'django-admin.py' thus the function
        require the django to be installed.
        It return True when the process successfully end, otherwise it print
        error messages and return False.
        https://docs.djangoproject.com/en/dev/ref/django-admin/#compilemessages
        """
        try:
            import django
        except ImportError:
            print('####################################################\n'
                  'Django is not installed.\nIt will not be possible to '
                  'compile the locale files during installation of '
                  'django-inspectional-registration.\nPlease, install '
                  'Django first. Done so, install the django-registration'
                  '-inspectional\n'
                  '####################################################\n')
            return False
        else:
            original_cwd = os.getcwd()
            BASE = os.path.abspath(os.path.dirname(__file__))
            root = os.path.join(BASE, 'author')
            os.chdir(root)
            os.system('django-admin.py compilemessages')
            os.chdir(original_cwd)
            return True

class sdist(original_sdist):
    """
    Run 'sdist' command but make sure that the message files are latest by
    running 'compile_messages' before 'sdist'
    """
    def run(self):
        compile_messages.compile_messages()
        original_sdist.run(self)

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
        'setuptools-git',
        ],
    test_suite = 'tests.runtests.runtests',
)
