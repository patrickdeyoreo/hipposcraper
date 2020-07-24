#!/usr/bin/env python3
"""
Install hipposcraper.

Usage:
    install.py [OPTIONS...]

Options:
    -g, --github=<github-profile-name>
        github profile

    -n, --name=<author-name>
        name of author

    -p, --password=<intranet-password>
        holberton password

    -u, --username=<intranet-username>
        holberton username
"""

import atexit
import argparse
import json
import logging
import os
import pathlib
import shutil
import signal
import sys

import hipposcraper

PACKAGE = hipposcraper.__package__
PROGRAM = PACKAGE

PKGSRC = hipposcraper.__path__[0]
PRGSRC = os.extsep.join((PKGSRC, 'py'))

PREFIX = os.path.join(os.path.expanduser('~'), '.local')

LOGGER = logging.getLogger(PACKAGE)


class InstallationDirectories:
    """Configure installation paths."""

    def __init__(self, package, prefix):
        """Initialize a configuration."""
        LOGGER.debug("Configuring installation directories for %s", package)
        self.__package = package
        self.__created = set()
        self.__mode = 0o777 & ~os.umask(0)
        LOGGER.info("File creation mode set to %03o (umask %03o)",
                    self.__mode, os.umask(0o777 & ~self.__mode))
        for path in sys.path:
            if path.startswith(prefix):
                LOGGER.debug("Setting python path to %s", path)
                self.__python_path = pathlib.Path(path)
                break
        else:
            raise ValueError('no path elements with prefix {}'.format(prefix))
        self.__paths = [getattr(self, name)
                        for name, value in vars(type(self)).items()
                        if isinstance(value, property)]

    @property
    def home(self):
        """Get user home directory"""
        return pathlib.Path.home()

    @property
    def bin(self):
        """Get user bin directory"""
        if (self.home / '.bin').exists():
            return self.home / '.bin'
        return self.home.joinpath('.local', 'bin')

    @property
    def data(self):
        """Get user data directory"""
        return pathlib.Path(os.getenv(
            'XDG_DATA_HOME',
            os.path.join(self.home, '.local', 'share')
        )).joinpath(self.__package)

    @property
    def config(self):
        """Get user config directory"""
        return pathlib.Path(os.getenv(
            'XDG_CONFIG_HOME',
            os.path.join(self.home, '.config')
        )).joinpath(self.__package)

    @property
    def cache(self):
        """Get user cache directory"""
        return pathlib.Path(os.getenv(
            'XDG_CACHE_HOME',
            os.path.join(self.home, '.cache')
        )).joinpath(self.__package)

    @property
    def python_path(self):
        """Get python path directory"""
        return self.__python_path

    def create_dirs(self):
        """Create directories"""
        LOGGER.info('Creating installation directories...')
        for path in self.__paths:
            try:
                path.mkdir(mode=self.__mode, parents=True)
                LOGGER.debug('Created %s', path)
                self.__created.add(path)
            except FileExistsError:
                LOGGER.debug('%s already exists', path)
        LOGGER.info('Directory creation complete.')

    def remove_dirs(self):
        """Remove directories created by the bound instance"""
        LOGGER.info('Removing installation directories...')
        for path in self.__created:
            try:
                shutil.rmtree(path)
                LOGGER.debug('Removed %s', path)
            except FileNotFoundError:
                LOGGER.debug('%s not found... where did it go?', path)
        LOGGER.info('Directory removal complete.')

    def commit_dirs(self):
        """Commit directory changes such that they may not be undone"""
        self.__created.clear()


def parse_args():
    """Parse command line arguments"""
    LOGGER.debug('Creating argument parser...')
    parser = argparse.ArgumentParser()
    parser.add_argument('-g', '--github', dest='github', default=None,
                        help='github profile')
    parser.add_argument('-n', '--name', dest='name', default=None,
                        help='name of author')
    parser.add_argument('-p', '--password', dest='password', default=None,
                        help='holberton intranet password')
    parser.add_argument('-u', '--username', dest='login', default=None,
                        help='holberton intranet username')
    LOGGER.debug('Parsing arguments: %s', str(sys.argv[1:]))
    return parser.parse_args()


def read_input(**kwgs):
    """Read arguments from stdin"""
    LOGGER.debug('Reading remaining arguments from stdin...')
    for name, value in kwgs.items():
        if value is None:
            kwgs[name] = input('{}: '.format(name))
    return kwgs

def main():
    """Install hipposcraper."""
    signal.signal(
        signal.SIGINT,
        lambda *_:
        print('Farewell.', file=sys.stderr) or sys.exit(signal.SIGINT))

    try:
        dirs = InstallationDirectories(PACKAGE, PREFIX)
        atexit.register(dirs.remove_dirs)
    except ValueError as exc:
        print(*exc.args, sep=': ', file=sys.stderr)
        sys.exit(1)

    data = read_input(**vars(parse_args()))
    dirs.create_dirs()
    LOGGER.info('Copying executable to %s ...', str(dirs.bin.joinpath(PROGRAM)))
    shutil.copyfile(PRGSRC, dirs.bin.joinpath(PROGRAM))
    LOGGER.info('Setting permissions on %s ...', str(dirs.bin.joinpath(PROGRAM)))
    os.chmod(dirs.bin.joinpath(PROGRAM), mode=0o755)
    LOGGER.info('Writing user configuration data under %s ...', str(dirs.config))
    with open(dirs.config / 'credentials.json', mode='w') as ostream:
        json.dump(data, ostream)
    LOGGER.info('Copying package tree into %s ...', str(dirs.python_path))
    shutil.copytree(PKGSRC, dirs.python_path.joinpath(PACKAGE))
    LOGGER.info('Committing directory changes ...')
    dirs.commit_dirs()
    LOGGER.info('Installation complete.')


if __name__ == '__main__':
    main()
