#!/usr/bin/env python3
"""
Scrape it.

usage: hipposcraper.py URL ...
"""
import sys

import hipposcraper  # pylint: disable=import-self


if __name__ == '__main__':
    sys.exit(hipposcraper.hipposcraper())  # pylint: disable=no-member
