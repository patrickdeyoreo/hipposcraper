#!/usr/bin/env python3
"""Provides the main entry point for the hipposcrape module."""
import sys

from . import hippodir
from . import hippodoc


def main():
    """
    Create the required files and generate a README for each project URL.
    """
    hippodir()
    hippodoc()


if __name__ == "__main__":
    sys.exit(main())
