#!/usr/bin/env python3
"""
hippodir entry point
usage: hippodir.py URL ...
"""
import argparse
import json
import pathlib
import sys

import hipposcraper
from . hippoconfig import Credentials, create_config
from . import scrapers


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(metavar='URL', nargs='+', dest='urls',
                        help='URLs of projects on intranet.hbtn.io')
    return parser.parse_args()


def set_permissions():
    """Set file permissions."""
    sys.stdout.write("  -> Setting permissions... ")
    for path in pathlib.Path('.').glob('*'):
        path.chmod(path.stat().st_mode & 0o7777 | 0o100)


def create_dir(url, credentials=None):
    """Create a directory for a project given its URL."""

    print("Creating project:")
    # Acquiring and parsing project data
    project_data = scrapers.BaseParse(url, credentials=credentials)
    project_type = project_data.project_type_check()

    # Creating scraping objects
    if "high" in project_type or "interview" in project_type:
        scraper = scrapers.HighScraper(project_data.soup)
    elif "low" in project_type or "linux" in project_type:
        scraper = scrapers.LowScraper(project_data.soup)
    elif "devops" in project_type:
        scraper = scrapers.SysScraper(project_data.soup)
    else:
        raise ValueError('Failed to determine project type.')

    # Creating project directory
    project_data.create_directory()
    # Writing to files with scraped data
    scraper.write_files()
    # Creating test (main) files
    scrapers.TestFileScraper(project_data.soup).write_test_files()

    print('Created project directory.')
    return project_data.dir_name


def hippodir():
    """
    Entry point for hippodir

    Scrapes project type (low level, high level, or system engineer),
    then it checks project type to execute appropriate scrapes.
    """
    args = parse_args()
    print("Hippodir (v{})".format(hipposcraper.__version__))
    try:
        user_data = Credentials(load=True)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = create_config()
    for url in args.urls:
        try:
            create_dir(url, credentials=user_data)
        except ValueError as err:
            if getattr(err, 'args', False):
                print('[ERROR]', *err.args, sep=': ', file=sys.stderr)


if __name__ == "__main__":
    sys.exit(hippodir())
