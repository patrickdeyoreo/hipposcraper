#!/usr/bin/env bash
# Run the Holberton project scraper on a link to a Holberton project.
#   The first argument provided to the script is expected to be a
#+  link to a Holberton School project.

project=$1
python3 ENTER_FULL_PATHNAME_TO_DIRECTORY_HERE/hippoproject.py "$project"
python3 ENTER_FULL_PATHNAME_TO_DIRECTORY_HERE/hipporead.py "$project"
