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
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '--user', '-r',
            str(pathlib.Path(__file__).absolute().parent / 'requirements.txt')
        ], check=True)
    except subprocess.CalledProcessError as err:
        sys.exit(err.returncode)
    import hipposcraper


THISDIR = pathlib.Path(__file__).absolute().parent
PACKAGE = hipposcraper.__package__
SCRIPTS = {
    'hippoconfig': THISDIR / 'hippoconfig.py',
    'hippodir': THISDIR / 'hippodir.py',
    'hippodoc': THISDIR / 'hippodoc.py',
    'hipposcraper': THISDIR / 'hipposcraper.py',
}

PKGDIR = pathlib.Path(hipposcraper.__file__).absolute().parent

logging.basicConfig(format='%(filename)s: %(message)s')

LOGGER = logging.getLogger(PACKAGE)
LOGGER.setLevel('DEBUG' if 'DEBUG' in os.environ else 'INFO')

signal.signal(signal.SIGINT, lambda *_: sys.exit(128 + signal.SIGINT))


class InstallationDirectories:
    """Prepare installation directories."""

    def __init__(self, package=PACKAGE):
        """Initialize an installation directory configuration."""
        LOGGER.info('Configuring installation directories for %s', package)
        self.__package = package
        self.__directories = {self.bin, self.config, self.site}
        self.__created = set()

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
        if isinstance(value, pathlib.Path):
            self.__directories.add(value)
        else:
            raise ValueError('Invalid path: {}'.format(value))

    def unregister_directory(self, value):
        """Discard an installation directory"""
        if isinstance(value, bytes):
            value = value.decode()
        if isinstance(value, str):
            value = pathlib.Path(value)
        if isinstance(value, pathlib.Path):
            self.__directories.discard(value)
        else:
            raise ValueError('Invalid path: {}'.format(value))

    def make_directories(self):
        """Create the installation directories"""
        LOGGER.debug('Enabling directory removal upon exit...')
        self.resetdirs = atexit.register(self.unmake_directories)
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
                LOGGER.warning('Removed %s', path)
            except FileNotFoundError:
                LOGGER.warning('%s not found... where did it go?', path)
        LOGGER.warning('Directory removal complete.')

    def commit_directories(self):
        """Commit directory changes such that they will not be undone."""
        LOGGER.debug('Disabling directory removal upon exit...')
        atexit.unregister(self.unmake_directories)
        self.__created.clear()
        LOGGER.debug('Directory changes committed.')


def main():
    """Install hipposcraper."""
    dirs = InstallationDirectories(PACKAGE)
    dirs.make_directories()
    hipposcraper.hippoconfig()
    LOGGER.debug('Credentials saved in %s', str(hipposcraper.CONFIG_HOME))
    LOGGER.debug('Removing Python bytecode from source tree...')
    for path in PKGDIR.rglob('__pycache__'):
        shutil.rmtree(path)
    LOGGER.debug('Python bytecode removed.')
    if (dirs.site / PACKAGE).exists():
        LOGGER.info('Removing existing installation...')
        shutil.rmtree(dirs.site / PACKAGE)
        LOGGER.debug('Installation removed.',)
    LOGGER.info('Installing package at %s...',  str(dirs.site / PACKAGE))
    shutil.copytree(PKGDIR, dirs.site / PACKAGE)
    LOGGER.debug('Package installed.',)
    for name, src in SCRIPTS.items():
        dest = dirs.bin / name
        LOGGER.info('Installing executable %s at %s...', name, str(dest))
        shutil.copyfile(src, dest)
        LOGGER.debug('%s installed.', name)
        LOGGER.debug('Setting file mode to %03o on %s...', 0o755, str(dest))
        dest.chmod(0o755)
    LOGGER.debug('Committing directory changes...')
    dirs.commit_directories()
    LOGGER.info('Installation complete.')


if __name__ == '__main__':
    sys.exit(main())
