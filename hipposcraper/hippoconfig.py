#!/usr/bin/env python3
"""
hippoconfig entry point
Usage:
    hippoconfig.py [OPTIONS...]

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
import argparse
import json
import os
import pprint
import sys

import hipposcraper
from . import configuration


def parse_kwargs():
    """Parse arguments passed by caller."""
    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--author-name', dest='author',
                        default=None, help='name of author')
    parser.add_argument('-g', '--github-user', dest='github_username',
                        default=None, help='github username')
    parser.add_argument('-u', '--holberton-user', dest='holberton_username',
                        default=None, help='holberton intranet username')
    parser.add_argument('-p', '--holberton-pass', dest='holberton_password',
                        default=None, help='holberton intranet password')
    kwargs = vars(parser.parse_args())
    return ((key, value) for key, value in kwargs.items() if value is not None)


def hippoconfig():
    """Create and modify user config."""
    print("Hippoconfig (v{})".format(hipposcraper.__version__))
    config = configuration.Credentials()
    if len(sys.argv) > 1:
        try:
            print("Loaded configuration from {}".format(
                config.load().replace(os.path.expanduser('~'), '~', 1)
            ))
            print('Existing config:')
            pprint.pprint(config)
        except FileNotFoundError:
            print("No config found.")
        except json.JSONDecodeError:
            print("Unable to load config from invalid JSON.")
        except OSError:
            print("Unable to load config.")
        print("Updating configuration...")
        config.update(parse_kwargs())
    else:
        config.update(
            (key, input('{}: '.format(config.info(key)))) for key in config)
    print("New config:")
    pprint.pprint(config)
    print("Saved configuration to {}".format(
        config.save().replace(os.path.expanduser('~'), '~', 1)
    ))


if __name__ == '__main__':
    hippoconfig()
