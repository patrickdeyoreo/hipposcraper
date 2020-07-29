#!/usr/bin/env python3
"""Module for BaseParse"""
import json
import os
import re
import sys

from bs4 import BeautifulSoup
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
        valid_link = "intranet.hbtn.io/projects"
        while valid_link not in value:
            print("[ERROR] Invalid url (must be on intranet.hbtn.io)")
            value = input("Enter url to project: ")
        self.__hbtn_link = value

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
                print("[ERROR] Login failed (are your credentials correct?")
                sys.exit()
        print("done")
        return soup

    def find_directory(self):
        """Method that scrapes for project's directory name

        Sets project's directory's name to `dir_name`
        """
        find_dir = self.soup.find(string=re.compile("Directory: "))
        find_dir_text = find_dir.next_element.text
        return find_dir_text

    def create_directory(self):
        """Method that creates appropriate directory"""
        sys.stdout.write("  -> Creating directory... ")
        try:
            os.makedirs(self.dir_name, mode=0o755, exist_ok=False)
            os.chdir(self.dir_name)
            print("done")
        except OSError:
            print("[ERROR] Failed to create directory - does it already exist?")
            sys.exit()

    def project_type_check(self):
        """Method that checks the project's type

        Checks for which scraper to use by scraping 'Github repository: '

        Returns:
            project (str): scraped project type
        """
        find_project = self.soup.find(string=re.compile("GitHub repository: "))
        project = find_project.next_sibling.text
        return project
