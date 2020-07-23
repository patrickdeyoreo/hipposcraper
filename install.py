#!/usr/bin/env python3
"""
Install hipposcraper.

Usage:
    install.py [OPTIONS...]

Options:
    -g, --github=<github-profile>
        github profile url or username

    -n, --name=<author-name>
        name of the author

    -p, --password=<intranet-password>
        holberton password

    -u, --username=<intranet-username>
        holberton username
"""

import argparse
import json
import os
import pathlib
import shutil
import sys


PACKAGE = 'hipposcraper'
SRC_DIR = pathlib.Path(__file__).absolute().parent
SRC_EXE = SRC_DIR.joinpath(os.extsep.join((PACKAGE, 'py')))
PRIVATE = 'auth_data.json'


class Home:
    """
    Manage a directory hierarchy compliant with the XDG base directory spec.
    """
    def __init__(self, name=''):
        """Initialize an installation hierarchy"""
        self.__name = name
        self.__mode = 0o777 & ~os.umask(0)
        os.umask(0o777 & ~self.__mode)
        self.__created = set()
        if self.home.joinpath('.bin').exists():
            self.__bin_path = self.home.joinpath('.bin')
        else:
            self.__bin_path = self.home.joinpath('.local', 'bin')

    @property
    @staticmethod
    def home():
        """Get user home directory"""
        return pathlib.Path.home()

    @property
    def bin_path(self):
        """Get user data directory"""
        return self.__bin_path

    @property
    def data_path(self):
        """Get user data directory"""
        return pathlib.Path(os.getenv(
            'XDG_DATA_HOME',
            str(self.home.joinpath('.local', 'share'))
        )).joinpath(self.__name)

    @property
    def config_path(self):
        """Get user config directory"""
        return pathlib.Path(os.getenv(
            'XDG_CONFIG_HOME',
            str(self.home.joinpath('.config'))
        )).joinpath(self.__name)

    @property
    def cache_path(self):
        """Get user cache directory"""
        return pathlib.Path(os.getenv(
            'XDG_CACHE_HOME',
            str(self.home.joinpath('.cache'))
        )).joinpath(self.__name)

    def create_paths(self):
        """Make required components of the hierarchy"""
        try:
            self.data_path.mkdir(mode=self.__mode, parents=True)
            self.__created.add(self.data_path)
        except FileExistsError:
            pass
        try:
            self.config_path.mkdir(mode=self.__mode, parents=True)
            self.__created.add(self.config_path)
        except FileExistsError:
            pass
        try:
            self.cache_path.mkdir(mode=self.__mode, parents=True)
            self.__created.add(self.cache_path)
        except FileExistsError:
            pass
        try:
            self.__bin_path.mkdir(mode=self.__mode, parents=True)
            self.__created.add(self.cache_path)
        except FileExistsError:
            pass


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument('g', 'github', dest='github', default=None,
                        help='github profile')
    parser.add_argument('n', 'name', dest='name', default=None,
                        help='name of author')
    parser.add_argument('p', 'password', dest='password', default=None,
                        help='holberton intranet password')
    parser.add_argument('u', 'username', dest='login', default=None,
                        help='holberton intranet username')
    return vars(parser.parse_args())


def main():
    """Install hipposcraper."""
    home = Home(name=PACKAGE)
    home.create_paths()
    data = parse_args()
    with open(home.config_path.joinpath(PRIVATE), mode='w') as ostream:
        json.dump(data, ostream)
    shutil.copyfile(SRC_EXE, home.bin_path.joinpath(PACKAGE))


if __name__ == '__main__':
    sys.exit(main())
