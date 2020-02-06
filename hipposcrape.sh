#!/usr/bin/env bash
# Run the Holberton project scraper and README generator
# Usage: hipposcrape.sh [project-url]

NAME="${BASH_SOURCE[0]##*/}"
FILE="${BASH_SOURCE[0]}"
PYTHON='python3'
SCRAPE='hippoproject.py'
README='hipporead.py'


################
# usage - print usage information
# ARGUMENTS:
#   None
# OPTIONS:
#   -h: print full help message
# GLOBALS
#   None
# LOCALS:
#   None
# RETURN:
#   None
################
usage()
{
  if [[ $1 == -h ]]
  then
    cat
  else
    sed 1q
  fi
  return 0
} << EOF
Usage: ${NAME} [project-url]

Holberton project scraper and README generator

Exit status:
    0 upon success
    1 upon failure scraping a project or generating a README
    2 upon invalid usage
EOF


################
# parseopts - parse script options
# ARGUMENTS:
#   None
# OPTIONS:
#   None
# GLOBALS:
#   NAME - program name
#   OPTIND - index of the next option to process
#   OPTARG - argument of the option being processed
# LOCALS:
#   option - option being processed
# RETURN:
#   None
################
parseopts()
{
  local option

  while getopts ':h' option
  do
    case "${option}" in
      'h')
        usage -h
        exit 2
        ;;
      '?')
        printf '%s: -%s: unrecognized option\n' "${NAME}" "${OPTARG}" 1>&2
        usage 1>&2
        exit 2
        ;;
      ':')
        printf '%s: -%s: missing required argument\n' "${NAME}" "${OPTARG}" 1>&2
        usage 1>&2
        exit 2
        ;;
    esac
  done
}


################
# main - run the hipposcraper
# ARGUMENTS:
#   None
# OPTIONS:
#   None
# GLOBALS:
#   NAME - program name
#   FILE - program path
#   PYTHON - python executable name
# LOCALS:
#   OPTIND - index of the next option to process
#   OPTARG - argument of the option being processed
#   urls - project URLs
# RETURN:
#   None
main()
{
  local OPTARG=""
  local OPTIND=1
  local urls=( )

  parseopts "$@"
  shift "$((OPTIND - 1))"

  if (( $# ))
  then
    urls=( "$@" )
  else
    read -p 'Project URL: ' -r 'urls[0]'
  fi

  for _ in "${urls[@]}"
  do
    "${PYTHON}" "${FILE%/*}/${SCRAPE}" "${_}"
    "${PYTHON}" "${FILE%/*}/${README}" "${_}"
  done
}


main "$@"
