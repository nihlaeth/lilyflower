#!/usr/bin/python
import os
from setuptools import setup, Command

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    """Fetch readme."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


class Doctest(Command):

    """Run sphinx doctests."""

    description = 'Run doctests with Sphinx'
    user_options = []
    target = 'doctest'
    output_dir = '.doc/build'

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from sphinx.application import Sphinx
        sph = Sphinx('./doc/source',  # source directory
                     './doc/source',  # directory containing conf.py
                     self.output_dir,  # output directory
                     './doc/build/doctrees',  # doctree directory
                     self.target)  # finally, specify the doctest builder'
        sph.build()


class BuildHtml(Doctest):

    """Build sphinx html documentation."""

    target = 'html'
    output_dir = './doc/build/html'


setup(
    name="lilyflower",
    version="0.0.1a1",
    author="Nihlaeth",
    author_email="info@nihlaeth.nl",
    description=("A python interface that sits on top of lilypond."),
    license="GPLv3",
    keywords="lilypond music score sheet notation",
    url="https://github.com/nihlaeth/lilyflower",
    packages=['lilyflower', 'doc'],
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst']},
    cmdclass={
        'doctest': Doctest,
        'html': BuildHtml},
    extras_require={
        'doctest': ['sphinx>=1.3.1'],
        'doc': ['sphinx>=1.3.1'],
        },
    test_suite='tests',
    tests_require=['nose'],

    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
