#!/usr/bin/env python3
"""
Install the Hipposcraper.
"""
# pylint: disable=invalid-name

import atexit
import importlib
import logging
import os
import pathlib
import shutil
import signal
import site
import subprocess
import sys


HERE = pathlib.Path(__file__).parent.resolve()

PACKAGE = 'hipposcraper'

SCRIPTS = list(HERE.glob('hippo*.py'))

PACKAGE_REQUIRE_FILE = HERE / 'requirements.txt'

VERSION_REQUIRE = '3.5'


class ColorFormatter(logging.Formatter):
    """Color messages based on level name."""

    def __init__(self, *args, colors=None, **kwgs):
        """Iniitalize a colored formatter."""
        super().__init__(*args, **kwgs)
        if colors is None:
            self.colors = dict(ERROR=1, INFO=2, WARNING=3, DEBUG=4, CRITICAL=5)
        else:
            self.colors = dict(colors)

    def format(self, record):
        """Format and color a log message."""
        n = self.colors.get(record.levelname)
        if n is None:
            seq = '{:c}[39m'.format(0x1b)
        else:
            seq = '{:c}[38;5;{:d}m'.format(0x1b, n)
        return ''.join((seq, super().format(record), '{:c}[0m'.format(0x1b)))


class InstallationDirs:
    """Prepare installation directories."""

    def __init__(self, package, make_directories=False):
        """Initialize an installation directory configuration."""
        self.__package = package
        self.__directories = {self.bin, self.site, self.config}
        self.__created = set()
        if make_directories is True:
            self.make_directories()

    @property
    def home(self):
        """Get the path of the user home directory"""
        return pathlib.Path.home()

    @property
    def bin(self):
        """Get user bin directory"""
        if (self.home / '.bin').is_dir():
            return self.home / '.bin'
        return self.home / '.local' / 'bin'

    @property
    def site(self):
        """Get the path of the user site direcotry"""
        return pathlib.Path(site.getusersitepackages())

    @property
    def config(self):
        """Get the path of the user config directory"""
        return pathlib.Path(os.getenv(
            'XDG_CONFIG_HOME',
            os.path.join(os.path.expanduser('~'), '.config')
        )).absolute() / self.__package

    @property
    def directories(self):
        """Get user bin directory"""
        return self.__directories.copy()

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
        atexit.register(self.unmake_directories)
        logging.info('Creating installation directories...')
        for path in self.directories:
            try:
                path.mkdir(parents=True)
                self.__created.add(path)
                logging.info('Created %s', path)
            except FileExistsError:
                logging.debug('%s already exists.', path)
        logging.debug('Directory creation complete.')

    def unmake_directories(self):
        """Remove directories created by the bound instance"""
        logging.warning('Removing newly-created installation directories...')
        for path in self.__created:
            try:
                shutil.rmtree(str(path))
                logging.warning('Removed %s', path)
            except FileNotFoundError:
                logging.warning('%s not found... where did it go?', path)
        logging.warning('Directory removal complete.')

    def commit_directories(self):
        """Commit directory changes such that they will not be undone."""
        atexit.unregister(self.unmake_directories)
        self.__created.clear()
        logging.debug('Directory changes committed.')


def install_requirements(stdout=None, stderr=None):
    """Installed required packages."""
    filename = str(PACKAGE_REQUIRE_FILE)
    argv = [sys.executable, '-m', 'pip', 'install', '--user', '-r', filename]
    return subprocess.run(argv, stdout=stdout, stderr=stderr, check=False)


def install_scripts(bin_path):
    """Install executable scripts."""
    for src in SCRIPTS:
        dest = bin_path / src.stem
        logging.info('Installing %s executable at %s ...', src.stem, dest)
        shutil.copyfile(str(src), str(dest))
        mode = dest.stat().st_mode & 0o7777 | 0o100
        logging.debug('Setting permissions to %03o on %s ...', mode, dest)
        logging.debug('%s installed.', src.stem)
        dest.chmod(mode)


def python_at_least_version(min_version):
    """Check the Python interpreter version."""
    min_version_info = map(int, min_version.split('.'))
    return all(m <= n for m, n in zip(min_version_info, sys.version_info))


def configure_logging(level='INFO', fmt='%(message)s', stream=None):
    """Add a stream handler to a logger."""
    handler = logging.StreamHandler(stream=stream)
    handler.setFormatter(ColorFormatter(fmt=fmt))
    handler.setLevel(level)
    logging.basicConfig(level=level, format=fmt, handlers=[handler])


def sigint_handler(_, __):
    """Exit upon receiving SIGINT."""
    sys.exit(128 + signal.SIGINT)


def main():
    """Install the Hipposcraper."""
    signal.signal(signal.SIGINT, sigint_handler)
    configure_logging(level='DEBUG' if 'DEBUG' in os.environ else 'INFO')
    logging.info("Checking Python version...")
    if not python_at_least_version(VERSION_REQUIRE):
        logging.error("Python does not meet installation requirements.")
        logging.warning("Requires at least version %s (current version is %s)",
                        VERSION_REQUIRE, sys.version[:sys.version.find(' ')])
        return 1
    logging.info("Installing required packages...")
    process = install_requirements(
        stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if process.returncode != 0:
        logging.error(process.stderr.decode())
        return process.returncode
    logging.info('Importing %s module...', PACKAGE)
    pkg = importlib.import_module(PACKAGE)
    name = pkg.__package__
    src = pathlib.Path(pkg.__file__).absolute().parent
    logging.debug('Package source tree: %s', src)
    dirs = InstallationDirs(name, make_directories=True)
    logging.debug('Removing bytecode from source tree...')
    for path in src.rglob('__pycache__'):
        shutil.rmtree(str(path))
    logging.debug('Bytecode removed.')
    dest = dirs.site / name
    if dest.exists():
        logging.debug('Found existing installation.')
        logging.debug('Removing...')
        shutil.rmtree(str(dest))
        logging.debug('Installation removed.',)
    logging.info('Installing %s package under %s ...', name, dest)
    shutil.copytree(str(src), str(dest))
    logging.debug('Package installed.',)
    install_scripts(dirs.bin)
    logging.debug('Committing directory changes...')
    dirs.commit_directories()
    logging.info('Installation complete.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
