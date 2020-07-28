#!/usr/bin/env python3
"""setuptools build script"""
import pathlib
import setuptools

here = pathlib.Path(__file__).parent.resolve()

setuptools.setup(
    name="hipposcraper",
    version="2.0.1",
    author="Patrick DeYoreo",
    author_email="pdeyoreo@gmail.com",
    description="Create Holberton School project skeletons and documentation.",
    long_description=here.joinpath('README.md').read_text(encoding='utf-8'),
    long_description_content_type="text/markdown",
    url="github.com/patrickdeyoreo/hipposcraper",
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
        'console_scripts': [
            'hipposcraper=hipposcraper:main',
            'hippodoc=hipposcraper:hippodoc',
            'hippodir=hipposcraper:hippodir',
            'hippoconfig=hipposcraper:hippoconfig',
        ],
    },
    python_requires='>=3.4',
    install_requires=[
        'beautifulsoup4 >=4.8.2, <5',
        'requests >=2.24, <3'
    ],
)
