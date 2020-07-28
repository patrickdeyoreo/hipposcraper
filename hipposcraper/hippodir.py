#!/usr/bin/env python3
"""
hippodir entry point
usage: hippodir.py URL ...
"""
import argparse
import os
import sys

import hipposcraper
from . import scrapers


def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(dest='urls', nargs='+', action='append', metavar='URL',
                        help='URLs of projects on intranet.hbtn.io')
    return parser.parse_args()


def set_permissions():
    """Method that sets permissions on files"""
    sys.stdout.write("  -> Setting permissions... ")
    try:
        os.system("chmod u+x *")
        print("done")
    except OSError:
        print("[ERROR] Failed to set permissions")


def create_dir(url, credentials=None):
    """Create a directory for a project given its URL."""
    print("Creating project:")
    parse_data = scrapers.BaseParse(url, credentials=credentials)

    parse_data.find_directory()
    parse_data.create_directory()

    project_type = parse_data.project_type_check()
    if "high" in project_type:
        # Creating scraping objects
        hi_scraper = scrapers.HighScraper(parse_data.soup)
        t_scraper = scrapers.TestFileScraper(parse_data.soup)

        # Writing to files with scraped data
        hi_scraper.write_files()

        # Creating test (main) files
        t_scraper.write_test_files()

    elif "low" in project_type:
        # Creating scraping objects
        lo_scraper = scrapers.LowScraper(parse_data.soup)
        t_scraper = scrapers.TestFileScraper(parse_data.soup)

        # Writing to files with scraped data
        lo_scraper.write_putchar()
        lo_scraper.write_header()
        lo_scraper.write_files()

        # Creating test (main) files
        t_scraper.write_test_files()

    elif "linux" in project_type:
        # Creating scraping objects
        lo_scraper = scrapers.LowScraper(parse_data.soup)
        t_scraper = scrapers.TestFileScraper(parse_data.soup)

        # Writing to files with scraped data
        lo_scraper.write_putchar()
        lo_scraper.write_header()
        lo_scraper.write_files()

        # Creating test (main) files
        t_scraper.write_test_files()

    elif "system" in project_type:
        # Creating scraping objects
        sy_scraper = scrapers.SysScraper(parse_data.soup)
        t_scraper = scrapers.TestFileScraper(parse_data.soup)

        # Creating test (main) files
        t_scraper.write_test_files()

        # Writing to files with scraped data
        sy_scraper.write_files()

    else:
        print("[ERROR]: Could not determine project type")
        sys.exit()

    set_permissions()
    print("Project all set!")


def hippodir():
    """
    Entry point for hippodir

    Scrapes project type (low level, high level, or system engineer),
    then it checks project type to execute appropriate scrapes.
    """
    args = parse_args()
    print("Hippodir (v{})".format(hipposcraper.__version__))
    for url in args.urls:
        create_dir(url)


if __name__ == "__main__":
    sys.exit(hippodir())
