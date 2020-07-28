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
import subprocess
import sys

try:
    import hipposcraper
except ImportError:
    cmd = (sys.executable, '-m', 'pip', 'install', '--user', '-r', 'requirements.txt')
    process = subprocess.run(cmd)
    if process.returncode != 0:
        sys.exit(1)
    import hipposcraper

PACKAGE = hipposcraper.__package__
PROGRAM = PACKAGE

PKGSRC = os.path.dirname(hipposcraper.__file__)
PRGSRC = os.extsep.join((PKGSRC, 'py'))

logging.basicConfig()

LOGGER = logging.getLogger(PACKAGE)
LOGGER.setLevel('DEBUG' if 'HIPPODEBUG' in os.environ else 'INFO')


class InstallationDirectories:
    """Prepare installation directories."""

    def __init__(self, package=PACKAGE):
        """Initialize an installation directory configuration."""
        LOGGER.info('Configuring installation directories for %s', package)
        self.__package = package
        self.__directories = {self.bin, self.config, self.site}
        self.__created = set()
        self.resetdirs = atexit.register(self.unmake_directories)

    @property
    def directories(self):
        """Get user bin directory"""
        return self.__directories.copy()

    @property
    def bin(self):
        """Get user bin directory"""
        if (self.home / '.bin').is_dir():
            return self.home / '.bin'
        return self.home / '.local' / 'bin'

    @property
    def config(self):
        """Get the path of the user config directory"""
        return pathlib.Path(hipposcraper.CONFIG_HOME)

    @property
    def home(self):
        """Get the path of the user home directory"""
        return pathlib.Path.home()

    @property
    def site(self):
        """Get the path of the user site direcotry"""
        return pathlib.Path(site.getusersitepackages())

    def register_directory(self, value):
        """Add an installation directory"""
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, str):
            value = pathlib.Path(value)
        if isinstance(value, path.Path):
            self.__directories.add(value)
        else:
            raise ValueError('Invalid path: {}'.format(value))

    def unregister_directory(self, value):
        """Discard an installation directory"""
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, str):
            value = pathlib.Path(value)
        if isinstance(value, path.Path):
            self.__directories.discard(value)
        else:
            raise ValueError('Invalid path: {}'.format(value))

    def make_directories(self):
        """Create the installation directories"""
        LOGGER.info('Creating directories...')
        for path in self.directories:
            try:
                path.mkdir(parents=True)
                self.__created.add(path)
                LOGGER.info('Created %s', path)
            except FileExistsError:
                LOGGER.info('%s already exists.', path)
        LOGGER.info('Directory creation complete.')

    def unmake_directories(self):
        """Remove directories created by the bound instance"""
        LOGGER.warning('Removing directories...')
        for path in self.__created:
            try:
                shutil.rmtree(path)
                LOGGER.warning('Removed: %s', path)
            except FileNotFoundError:
                LOGGER.warning('%s not found... where did it go?', path)
        LOGGER.info('Directory removal complete.')

    def commitdirs(self):
        """Commit directory changes such that they will not be undone."""
        self.__created.clear()
        LOGGER.debug('Directory changes committed.')


def main():
    """Install hipposcraper."""
    dirs = InstallationDirectories(PACKAGE)
    dirs.make_directories()
    signal.signal(signal.SIGINT, lambda *_: sys.exit(128 + signal.SIGINT))
    LOGGER.info('Installing executable in %s', str(dirs.bin))
    shutil.copyfile(PRGSRC, dirs.bin / PROGRAM)
    LOGGER.info('Setting file mode on %s', str(dirs.bin / PROGRAM))
    os.chmod(dirs.bin / PROGRAM, mode=0o755)
    hipposcraper.hippoconfig()
    LOGGER.info('Credentials saved in %s', str(hipposcraper.CONFIG_HOME))
    pkgdir = dirs.site / PACKAGE
    if pkgdir.exists():
        LOGGER.info('Removing old package directory...')
        shutil.rmtree(pkgdir, ignore_errors=True)
    LOGGER.info('Installing package in %s', str(pkgdir))
    shutil.copytree(PKGSRC, os.path.join(site.getusersitepackages(), PACKAGE))
    LOGGER.info('Committing directory changes...')
    dirs.commitdirs()
    LOGGER.info('Installation complete.')


if __name__ == '__main__':
    main()
