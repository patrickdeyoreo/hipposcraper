#!/usr/bin/env python3
"""
hippodoc entry point
usage: hippodoc.py URL ...
"""
import argparse
import sys

import hipposcraper
from . import scrapers


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='urls', nargs='+', action='append', metavar='URL',
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

    author = parse_data.json_data['author']
    user = parse_data.json_data['github_username']
    r_scraper.write_footer(author, user, 'github.com/{}'.format(user))

    print("README.md all set!")


def hippodoc():
    """
    Entry point for hippodoc

    Scrapes for specific text to create a README automatically.
    """
    args = parse_args()
    print("Hippodoc (v{})".format(hipposcraper.__version__))
    for url in args.urls:
        create_doc(url)


if __name__ == "__main__":
    sys.exit(hippodoc())
