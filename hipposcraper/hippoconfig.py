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
from . config import Credentials


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
    args = parser.parse_args()
    return {key: arg for key, arg in vars(args).items() if arg is not None}


def create_config(**kwgs):
    """Create and update hipposcraper config."""
    user_data = Credentials(load=False)
    try:
        print("Loaded config from {}".format(
            user_data.load().replace(os.path.expanduser('~'), '~', 1)
        ))
        print('Configuration:')
        pprint.pprint(user_data)
    except FileNotFoundError:
        print("No existing config found.")
    except json.JSONDecodeError:
        print("Unable to load config from invalid JSON.")
    except OSError:
        print("Unable to load config.")
    if not kwgs:
        kwgs = {
            key: input('{}: '.format(user_data.info(key))) or value
            for key, value in user_data.items()
        }
    print("Updating config...")
    user_data.update(kwgs)
    print("Configuration:")
    pprint.pprint(user_data)
    print("Saved configuration to {}".format(
        user_data.save().replace(os.path.expanduser('~'), '~', 1)
    ))
    return user_data


def hippoconfig():
    """
    Entry point for hippoconfig.

    Create and update user configuration data.
    """
    kwargs = parse_kwargs()
    print("Hippoconfig (v{})".format(hipposcraper.__version__))
    create_config(**kwargs)


if __name__ == '__main__':
    sys.exit(hippoconfig())
