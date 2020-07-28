#!/usr/bin/env python3
"""Provides the main entry point for the hipposcraper module."""
import argparse
import json
import sys

from . config import Credentials
from . hippoconfig import hippoconfig
from . hippodir import create_dir
from . hippodoc import create_doc


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='urls', nargs='+', metavar='URL',
                        help='URLs of projects on intranet.hbtn.io')
    return parser.parse_args()


def main():
    """
    Create the required files and generate a README for each project URL.
    """
    args = parse_args()
    try:
        credentials = Credentials(load=True)
    except (FileNotFoundError, json.JSONDecodeError):
        hippoconfig()
        credentials = Credentials(load=True)
    for url in args.urls:
        create_dir(url, credentials=credentials)
        create_doc(url, credentials=credentials)


if __name__ == "__main__":
    sys.exit(main())
