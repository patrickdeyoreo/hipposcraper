#!/usr/bin/env python3
"""Provides the main entry point for the hipposcraper module."""
import sys

from . hippodir import hippodir
from . hippodoc import hippodoc


def main():
    """
    Create the required files and generate a README for each project URL.
    """
    hippodir()
    hippodoc()


if __name__ == "__main__":
    sys.exit(main())
