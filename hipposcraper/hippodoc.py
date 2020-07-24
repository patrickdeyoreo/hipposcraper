#!/usr/bin/env python3
"""
hippodoc entry point
usage: hippodoc.py URL ...
"""
import sys

from . import scrapers


def get_args():
    """Method that grabs argv

    Returns:
        link (str): argv[1]
    """
    arg = sys.argv[1:]
    count = len(arg)

    if count > 1:
        print("[ERROR] Too many arguments (must be one)")
        sys.exit()
    elif count == 0:
        print("[ERROR] Too few arguments (must be one)")
        sys.exit()

    link = sys.argv[1]
    return link


def hippodoc():
    """Entry point for hipporeader

    Scrapes for specific text to create a README automatically.
    """

    link = get_args()

    print("\nHipposcraper version 1.1.1")
    print("Creating README.md file:")
    parse_data = scrapers.BaseParse(link)

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

    author = parse_data.json_data["name"]
    user = parse_data.json_data["github"]
    git_link = "/".join(("github.com", parse_data.json_data["github"]))

    r_scraper.write_footer(author, user, git_link)

    print("README.md all set!")


if __name__ == "__main__":
    hippodoc()
