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
    __iteminfo = {
        'author': 'Name of author',
        'github_username': 'GitHub username',
        'holberton_username': 'Holberton login',
        'holberton_password': 'Holberton password',
    }

    def __init__(self, load=False, ignore_errors=()):
        """Initialize a credentials dictionary."""
        super().__init__((key, None) for key in self.__iteminfo)
        if load:
            self.load(ignore_errors=ignore_errors)

    def __setitem__(self, key, value):
        """Only set the values of known keys."""
        if key not in self.__iteminfo:
            raise KeyError('Bad credential key: {}'.format(key))
        super().__setitem__(key, value)

    @property
    def basename(self):
        """Get the name of the credentials file."""
        return self.__basename

    @property
    def dirname(self):
        """Get a path to the config directory."""
        return hipposcraper.CONFIG_HOME

    @property
    def path(self):
        """Get a path to the credentials file."""
        return os.path.join(self.dirname, self.basename)

    def info(self, key):
        """Get a description of a credential."""
        if key not in self.__iteminfo:
            raise KeyError('Bad credential key: {}'.format(key))
        return self.__iteminfo[key]

    def save(self, ignore_errors=()):
        """Save credentials and return the path."""
        ignore_errors = tuple(ignore_errors)
        try:
            if not os.path.isdir(self.dirname):
                os.remove(self.dirname)
        except FileNotFoundError:
            pass
        try:
            if not os.path.isdir(self.dirname):
                os.mkdir(self.dirname)
        except FileExistsError:
            pass
        try:
            with open(self.path, 'w') as ostream:
                print(json.dumps(self), file=ostream)
        except ignore_errors:
            pass
        return self.path

    def load(self, ignore_errors=()):
        """Load credentials and return the path."""
        ignore_errors = tuple(ignore_errors)
        try:
            with open(self.path, 'r') as istream:
                self.update(json.load(istream))
        except ignore_errors:
            pass
        return self.path
