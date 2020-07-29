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
    parse_data = scrapers.BaseParse(url, credentials=credentials)

    parse_data.find_directory()
    parse_data.create_directory()

    project_type = parse_data.project_type_check()
    if "high" in project_type:
        # Creating scraping objects
        scraper = scrapers.HighScraper(parse_data.soup)

    elif "low" in project_type:
        # Creating scraping objects
        scraper = scrapers.LowScraper(parse_data.soup)

        # Writing files exclusive to low-level projects
        scraper.write_putchar()
        scraper.write_header()

    elif "linux" in project_type:
        # Creating scraping objects
        scraper = scrapers.LowScraper(parse_data.soup)

        # Writing files exclusive to low-level projects
        scraper.write_putchar()
        scraper.write_header()

    elif "system" in project_type:
        # Creating scraping objects
        scraper = scrapers.SysScraper(parse_data.soup)

    else:
        raise ValueError('Failed to determine project type.')

    # Writing to files with scraped data
    scraper.write_files()

    # Creating test (main) files
    scrapers.TestFileScraper(parse_data.soup).write_test_files()

    print('Created project directory.')

    return parse_data.dir_name


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
