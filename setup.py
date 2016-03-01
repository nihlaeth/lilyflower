import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...


def read(fname):
    """Fetch readme."""
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="lilyflower",
    version="0.0.1a1",
    author="Nihlaeth",
    author_email="info@nihlaeth.nl",
    description=("A python interface that sits on top of lilypond."),
    license="GPLv3",
    keywords="lilypond music score sheet notation",
    url="https://github.com/nihlaeth/lilyflower",
    packages=['lilyflower'],
    long_description=read('README.md'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
