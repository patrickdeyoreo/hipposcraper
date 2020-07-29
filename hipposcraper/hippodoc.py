#!/usr/bin/env python3
"""
hippodoc entry point
usage: hippodoc.py URL ...
"""
import argparse
import json
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


def create_doc(url, credentials=None):
    """Create a README for a project given its URL."""
    print("Creating README.md:")
    parse_data = scrapers.BaseParse(url, credentials=credentials)

    sys.stdout.write("  -> Scraping information... ")
    # Creating scraping object
    r_scraper = scrapers.ReadScraper(parse_data.soup)

    print("done")

    # Writing to README.md with scraped data
    r_scraper.open_readme()
    r_scraper.write_title()
    r_scraper.write_rsc()
    r_scraper.write_info()
    r_scraper.write_tasks()

    author = parse_data.user_data['author']
    user = parse_data.user_data['github_username']
    r_scraper.write_footer(author, user, 'github.com/{}'.format(user))

    print("README.md all set!")

    return r_scraper.readme


def hippodoc():
    """
    Entry point for hippodoc

    Scrapes for specific text to create a README automatically.
    """
    args = parse_args()
    print("Hippodoc (v{})".format(hipposcraper.__version__))
    try:
        user_data = Credentials(load=True)
    except (FileNotFoundError, json.JSONDecodeError):
        user_data = create_config()
    for url in args.urls:
        try:
            create_doc(url, credentials=user_data)
        except ValueError as err:
            if getattr(err, 'args', False):
                print('[ERROR]', *err.args, sep=': ', file=sys.stderr)


if __name__ == "__main__":
    sys.exit(hippodoc())
