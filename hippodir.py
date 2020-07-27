#!/usr/bin/env python3
"""
Scrape it.

usage: hippodir.py URL ...
"""
import sys

import hipposcraper


if __name__ == '__main__':
    sys.exit(hipposcraper.hippodir())
