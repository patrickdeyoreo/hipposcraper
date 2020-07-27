#!/usr/bin/env python3
"""
Scrape it.

usage: hippodoc.py URL ...
"""
import sys

import hipposcraper


if __name__ == '__main__':
    sys.exit(hipposcraper.hippodoc())
