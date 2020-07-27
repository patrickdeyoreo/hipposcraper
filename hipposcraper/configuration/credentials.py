#!/usr/bin/env python3
"""
Configure user credentials.
"""
import json
import os

import hipposcraper


class Credentials(dict):
    """
    Save, load, and allow access to hipposcraper credentials.
    """
    __basename = 'credentials.json'
    __datainfo = {
        'author': 'Name of author',
        'github_username': 'GitHub username',
        'holberton_username': 'Holberton username',
        'holberton_password': 'Holberton password',
    }

    def __init__(self, load=False, **kwgs):
        """Initialize a credentials dictionary."""
        super().__init__((key, kwgs.get(key)) for key in self.__datainfo)
        if load:
            self.load()

    def __setitem__(self, key, value):
        """Only set the values of recognized items."""
        if key not in self.__datainfo:
            raise KeyError("Bad credential key")
        super().__setitem__(key, value)

    def __delitem__(self, key):
        """Reset values rather than removing items."""
        if key in self.__datainfo:
            super().__setitem__(key, None)
        else:
            super().__delitem__(key)

    @property
    def path(self):
        """Get the path to the credential config file."""
        return os.path.join(hipposcraper.CONFIG_HOME, self.__basename)

    def info(self, key):
        """Get a description of a credential item."""
        if key not in self.__datainfo:
            raise KeyError("Bad credential key")
        return self.__datainfo[key]

    def load(self):
        """Load credentials and return the path."""
        with open(self.path, 'r') as istream:
            self.update(**json.load(istream))
        return self.path

    def save(self):
        """Save credentials and return the path."""
        with open(self.path, 'w') as ostream:
            json.dump(dict(self), ostream)
            print(file=ostream)
        return self.path
