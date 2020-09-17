#!/usr/bin/env python3
"""
Create Holberton School project skeletons and documentation.
"""
import os
import logging

from . hippoconfig import hippoconfig
from . hippodir import hippodir
from . hippodoc import hippodoc
from . main import main

__license__ = 'GPL3'
__version__ =  '2.0.4'

LOGGER = logging.getLogger(__name__)

CONFIG_HOME = os.path.join(os.path.abspath(os.getenv(
    'XDG_CONFIG_HOME',
    os.path.join(os.path.expanduser('~'), '.config')
)), __package__)
