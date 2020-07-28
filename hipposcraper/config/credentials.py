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
        'holberton_username': 'Holberton username',
        'holberton_password': 'Holberton password',
    }

    def __init__(self, load=False, ignore_errors=(), **kwgs):
        """Initialize a credentials dictionary."""
        ignore_errors = tuple(ignore_errors)
        if load:
            try:
                with open(self.path, 'r') as istream:
                    kwgs.update({
                        key: value for key, value in json.load(istream).items()
                        if key not in kwgs
                    })
            except ignore_errors:
                pass
        super().__init__({key: kwgs.get(key) for key in self.__iteminfo})

    def __setitem__(self, key, value):
        """Only set the values of recognized items."""
        if key not in self.__iteminfo:
            raise KeyError('Bad credential key: {}'.format(key))
        super().__setitem__(key, value)

    def __delitem__(self, key):
        """Reset values rather than removing items."""
        if key in self.__iteminfo:
            super().__setitem__(key, None)
        else:
            super().__delitem__(key)

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

    def load(self, ignore_errors=()):
        """Load credentials and return the path."""
        ignore_errors = tuple(ignore_errors)
        try:
            with open(self.path, 'r') as istream:
                self.update({
                    key: value for key, value in json.load(istream).items()
                    if key in self.__iteminfo
                })
        except ignore_errors:
            pass
        return self.path

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
                json.dump(self, ostream)
                print(file=ostream)
        except ignore_errors:
            pass
        return self.path
