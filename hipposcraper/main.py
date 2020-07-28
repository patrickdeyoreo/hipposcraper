#!/usr/bin/env python3
"""Provides the main entry point for the hipposcraper module."""
import argparse
import json
import sys

from . config import Credentials
from . hippoconfig import hippoconfig
from . hippodir import hippodir
from . hippodoc import hippodoc


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='urls', nargs='+', action='append', metavar='URL',
                        help='URLs of projects on intranet.hbtn.io')
    return parser.parse_args()


def main():
    """
    Create the required files and generate a README for each project URL.
    """
    args = parse_args()
    del sys.argv[1:]
    try:
        Credentials(load=True)
    except (FileNotFoundError, json.JSONDecodeError):
        hippoconfig()
    for url in args.urls:
        sys.argv.append(url)
        hippodir()
        hippodoc()
        del sys.argv[1:]


if __name__ == "__main__":
    sys.exit(main())
