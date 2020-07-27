#!/usr/bin/env python3
"""
Install hipposcraper.

Usage:
    install.py [OPTIONS...]

Options:
    -a, --author=<author-name>
        name of the author

    -g, --github=<github-username>
        github unsername

    -p, --password=<holberton-password>
        holberton intranet password

    -u, --username=<holberton-username>
        holberton intranet username
"""

import atexit
import json
import logging
import os
import pathlib
import shutil
import signal
import site
import sys

import hipposcraper

PACKAGE = hipposcraper.__package__
PROGRAM = PACKAGE

PKGSRC = os.path.dirname(hipposcraper.__file__)
PRGSRC = os.extsep.join((PKGSRC, 'py'))

logging.basicConfig()

LOGGER = logging.getLogger(PACKAGE)
LOGGER.setLevel('INFO')


class InstallationDirectories:
    """Prepare installation directories."""

    def __init__(self, package=PACKAGE):
        """Initialize an installation directory configuration."""
        LOGGER.info('Configuring installation directories for: %s', package)
        self.__package = package
        self.__created = set()
        self.resetdirs = atexit.register(self.resetdirs)

    @property
    def bin(self):
        """Get user bin directory"""
        if (self.home / '.bin').exists():
            return self.home / '.bin'
        return self.home / '.local' / 'bin'

    @property
    def config(self):
        """Get user config directory"""
        return pathlib.Path(hipposcraper.CONFIG_HOME)

    @property
    def home(self):
        """Get user home directory"""
        return pathlib.Path.home()

    @property
    def site(self):
        """Get user site direcotry"""
        return pathlib.Path(site.getusersitepackages())

    @property
    def directories(self):
        """Get an iterable of all installation directories"""
        return [x for x in vars(self).values() if isinstance(x, pathlib.Path)]

    def makedirs(self):
        """Create installation directories"""
        LOGGER.info('Creating installation directories...')
        for path in self.directories:
            try:
                path.mkdir(parents=True)
                self.__created.add(path)
                LOGGER.info('Created: %s', path)
            except FileExistsError:
                LOGGER.info('%s already exists', path)
        LOGGER.info('Directory creation complete.')

    def resetdirs(self):
        """Remove directories created by the bound instance"""
        LOGGER.warning('Removing installation directories...')
        for path in self.__created:
            try:
                shutil.rmtree(path)
                LOGGER.warning('Removed: %s', path)
            except FileNotFoundError:
                LOGGER.warning('%s not found... where did it go?', path)
        LOGGER.info('Directory removal complete.')

    def commitdirs(self):
        """Commit directory changes such that they may not be undone"""
        self.__created.clear()


def main():
    """Install hipposcraper."""
    dirs = InstallationDirectories(PACKAGE)
    dirs.makedirs()
    signal.signal(signal.SIGINT, lambda *_: sys.exit(128 + signal.SIGINT))
    LOGGER.info('Installing executable under: %s', str(dirs.bin))
    shutil.copyfile(PRGSRC, dirs.bin / PROGRAM)
    LOGGER.info('Setting file mode on: %s', str(dirs.bin))
    os.chmod(dirs.bin / PROGRAM, mode=0o755)
    credentials = hipposcraper.hippoconfig()
    LOGGER.info('Credentials credentials written to: %s', str(credentials.filename))
    LOGGER.info('Installing package under: %s', str(dirs.site))
    shutil.copytree(PKGSRC, os.path.join(site.getusersitepackages(), PACKAGE))
    LOGGER.info('Committing directory changes...')
    dirs.commitdirs()
    LOGGER.info('Installation complete.')


if __name__ == '__main__':
    main()
