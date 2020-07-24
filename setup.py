#!/usr/bin/env python3
"""setuptools build script"""
import pathlib
from setuptools import setup, find_packages

here = pathlib.Path(__file__).parent.resolve()

try:
    long_description = (here / 'README.md').read_text(encoding='utf-8')
except FileNotFoundError:
    long_description = ''

setup(
    name="hipposcraper",
    version="1.1.1",
    author="Patrick DeYoreo",
    author_email="pdeyoreo@gmail.com",
    description="Create Holberton project skeletons and documentation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="github.com/patrickdeyoreo/hipposcraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL version 3",
        "Operating System :: OS Independent",
    ],
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'hipposcraper=hipposcraper:main',
        ],
    },
    package_data={
        'hipposcraper': [
            'templates/*',
        ],
    },
    python_requires='>=3.5',
    install_requires=[
        'beautifulsoup4',
    ],
)
