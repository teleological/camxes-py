

import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "camxes",
    version = "0.6",
    author = "Riley Martinez-Lynch",
    author_email = "camxes@alexburka.com",
    description = ("PEG parser and associated tools for Lojban"),
    license = "MIT",
    keywords = "lojban parser peg",
    url = "http://github.com/teleological/camxes-py",
    py_modules=['camxes'],
    data_files=[('jvs', ['jvs/en.xml'])],
    long_description=read('README.txt'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=['parsimonious', 'lxml']
)



