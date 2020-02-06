#!/usr/bin/env python3
"""Module for BaseParse"""
from scrapers import *


class BaseParse(object):
    """BaseParse class

    Contains read json data, and parsed html data for the scrapers
    to use. Also contains general methods to initialize the scrape.

    Args:
        link (str): link to the project page to scrape

    Attributes:
        json_data (dict): read json data from auth_data.json
        soup (obj): BeautifulSoup obj containing parsed link
        dir_name (str): directory name of the link
    """

    def __init__(self, link=""):
        self.htbn_link = link
        self.json_data = self.get_json()
        self.soup = self.get_soup()
        self.dir_name = self.find_directory()

    @htbn_link.setter
    def htbn_link(self, value):
        """Setter for htbn link

        Must contain holberton's url format for projects.

        Args:
            value (str): comes from argv[1] as the project link
        """
        valid_link = "intranet.hbtn.io/projects"
        while valid_link not in value:
            print("[ERROR] Invalid link (must be on intranet.hbtn.io)")
            value = input("Enter link to project: ")
        self.htbn_link = value

    def get_json(self):
        """Method that reads auth_data.json.

        Sets json read to `json_data`
        """
        super_path = os.path.dirname(os.path.abspath(__file__))
        try:
            with open("{}/auth_data.json".format(super_path.rsplit("/", 1)[0]), "r") as json_file:
                return json.load(json_file)
        except IOError:
            print("[ERROR] Please run ./setup.sh to setup your auth data...")
            sys.exit()

    def get_soup(self):
        """Method that parses the `htbn_link` with BeautifulSoup

        Initially logs in the intranet using mechanize and cookiejar.
        Then requests for the html of the link, and sets it into `soup`.

        Returns:
            soup (obj): BeautifulSoup parsed html object
        """
        login = "https://intranet.hbtn.io/auth/sign_in"
        cj = cookielib.CookieJar()
        with requests.Session() as session:
            auth = {
                'url': 'https://intranet.hbtn.io/auth/sign_in',
                'data': {
                    'user[login]': self.json_data.get(
                        'intra_user_key'
                    ),
                    'user[password]': self.json_data.get(
                        'intra_pass_key'
                    ),
                },
            }
            soup = BeautifulSoup(session.get(auth_url).content)
            sys.stdout.write("  -> Logging in... ")
            try:
                keys = [
                    'authenticity_token',
                    'commit',
                ]
                auth['data']['authenticity_token'] = soup.find(
                    'input', {'name': 'authenticity_token'})['value']
                auth['data']['commit'] = soup.find(
                    'input', {'name': 'commit'})['value']
                session.post(**auth)
                soup = BeautifulSoup(session.get(self.htbn_link).content)
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
            os.mkdir(self.dir_name)
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
