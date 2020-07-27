#!/usr/bin/env python3
"""
Configure it.

usage: hippodoc.py URL ...
"""
import sys

import hipposcraper


if __name__ == '__main__':
    sys.exit(hipposcraper.hippoconfig())
