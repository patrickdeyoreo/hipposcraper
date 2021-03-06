#!/usr/bin/env python3
"""setuptools build script"""
import os
import setuptools

THISDIR = os.path.abspath(os.path.dirname(__file__))

try:
    with open(os.path.join(THISDIR, "README.md")) as istream:
        LONG_DESCRIPTION = istream.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ""

setuptools.setup(
    name="hipposcraper",
    version="2.1.1",
    author="Patrick DeYoreo",
    author_email="pdeyoreo@gmail.com",
    description="Create Holberton School project skeletons and documentation.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/patrickdeyoreo/hipposcraper",
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU GPL version 3",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
    ],
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "hipposcraper=hipposcraper:hipposcraper",
            "hippodoc=hipposcraper:hippodoc",
            "hippodir=hipposcraper:hippodir",
            "hippoconfig=hipposcraper:hippoconfig",
        ],
    },
    install_requires=[
        "beautifulsoup4 >=4.8.2",
        "requests >=2.24",
    ],
    python_requires=">=3.4",
)
