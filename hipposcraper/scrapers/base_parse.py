#!/usr/bin/env python3
"""Module for BaseParse"""
import json
import os
import re
import sys

from bs4 import BeautifulSoup, Tag
import requests

from .. config import Credentials


class BaseParse(object):
    """
    Contains read json data, and parsed html data for the scrapers
    to use. Also contains general methods to initialize the scrape.

    Args:
        url (str): url to the project page to scrape

    Attributes:
        user_data (dict): read json data from credentials.json
        soup (obj): BeautifulSoup obj containing parsed url
        dir_name (str): directory name of the url
    """

    def __init__(self, url, credentials=None):
        self.hbtn_link = url
        self.user_data = credentials or Credentials(load=True)
        self.soup = self.get_soup()
        self.dir_name = self.find_directory()

    @property
    def hbtn_link(self):
        """Getter for hbtn url

        Returns:
            hbtn_link (str): value of the corresponding private attribute
        """
        return self.__hbtn_link

    @hbtn_link.setter
    def hbtn_link(self, value):
        """Setter for hbtn url

        Must contain holberton's url format for projects.

        Args:
            value (str): comes from argv[1] as the project url
        """
        host = 'intranet.hbtn.io'
        if value.find('://'):
            *_, value = value.partition('://')
        if not value.startswith('{}/'.format(fqdn)):
            raise ValueError("[ERROR] Host must be {}".format(host))
        self.__hbtn_link = 'https://{}'.format(value)

    def get_soup(self):
        """Method that parses the `hbtn_link` with BeautifulSoup

        Then requests for the html of the url, and sets it into `soup`.

        Returns:
            soup (obj): BeautifulSoup parsed html object
        """
        with requests.Session() as session:
            auth_url = 'https://intranet.hbtn.io/auth/sign_in'
            resp = session.get(auth_url)
            soup = BeautifulSoup(resp.content, features='html.parser')
            credentials = {
                'user[login]': self.user_data.get('holberton_username'),
                'user[password]': self.user_data.get('holberton_password'),
                'authenticity_token': soup.find(
                    'input', {'name': 'authenticity_token'}
                ).get('value'),
                'commit': soup.find(
                    'input', {'name': 'commit'}
                ).get('value'),
            }
            try:
                sys.stdout.write("  -> Logging in... ")
                session.post(auth_url, data=credentials)
                resp = session.get(self.hbtn_link)
                soup = BeautifulSoup(resp.content, features='html.parser')
            except AttributeError:
                print("[ERROR] Login failed. Check your credentials.")
                sys.exit()
        print("done")
        return soup

    def find_directory(self):
        """Scrape project directory names."""
        anchor = self.soup.find(string=re.compile("Directory: "))
        if isinstance(anchor, Tag) and isinstance(anchor.next_element, Tag):
            return anchor.next_element.text
        return None

    def create_directory(self):
        """Create appropriate directory trees."""
        print("  -> Creating directory {}".format(self.dir_name))
        try:
            os.makedirs(self.dir_name, mode=0o755, exist_ok=False)
            os.chdir(self.dir_name)
            print("done")
        except OSError:
            print("[ERROR] Failed to create directory. Does it already exist?")
            raise

    def project_type_check(self):
        """Scrape project types."""
        anchor = self.soup.find(string=re.compile("GitHub repository: "))
        if isinstance(anchor, Tag) and isinstance(anchor.next_sibling, Tag):
            return anchor.next_sibling.text
        return None
