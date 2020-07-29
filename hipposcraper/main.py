#!/usr/bin/env python3
"""Provides the main entry point for the hipposcraper module."""
import argparse
import json
import sys

from . hippoconfig import Credentials, create_config
from . hippodir import create_dir
from . hippodoc import create_doc


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='URL', nargs='+', dest='urls',
                        help='URLs of projects on intranet.hbtn.io')
    return parser.parse_args()


def main():
    """
    Create the required files and generate a README for each project URL.
    """
    args = parse_args()
    try:
        user_data = Credentials(load=True)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = create_config()
    for url in args.urls:
        create_dir(url, credentials=user_data)
        create_doc(url, credentials=user_data)


if __name__ == "__main__":
    sys.exit(main())
