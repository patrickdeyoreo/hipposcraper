#!/usr/bin/env python3
"""
Create Holberton School project skeletons and documentation.
"""
import os

from . main import main, hippoconfig, hippodir, hippodoc

__license__ = 'GPL3'
__version__ = '2.0.0'

CONFIG_HOME = os.path.join(os.path.abspath(os.getenv(
    'XDG_CONFIG_HOME', os.path.join(os.path.expanduser('~'), '.config')
)), __package__)
