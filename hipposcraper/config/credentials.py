#!/usr/bin/env python3
"""Configure user credentials."""
import json
import os
import pathlib
import sys

CREDENTIALS_FILE=os.path.join(os.getenv(
    'XDG_CONFIG_DIR',
    os.path.join(os.path.expanduser('~'), '.config')
), 'hipposcraper', 'credentials.json')

try:
    with open(CREDENTIALS_FILE) as istream:
        CREDENTIALS = json.load(istream)
except FileNotFoundError:
    print(sys.argv[0], CREDENTIALS_FILE, 'No such file', sep=': ')
    sys.exit(1)
except json.JSONDecodeError:
    print(sys.argv[0], CREDENTIALS_FILE, 'Invalid JSON', sep=': ')
    sys.exit(1)
