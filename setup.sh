#!/usr/bin/env sh
# Sets up the hipposcraper:
#+  Configures aliases in .bashrc
#+  Sets inputted user information in auth.json

AUTH_FILE='auth_data.json'

if test "$(id -u)" -eq 0; then
  2>&1 printf '%s: refusing to execute as root\n' "$0"
  exit 1
fi

escape_json_data() {
  printf '%s' "$1" | sed 's:["\]:\\&:g'
}

write_auth_data() {
  cat > "${AUTH_FILE}"
} << EOF
{
  "author_name": "$(escape_json_data "${author_name}")",
  "intra_user_key": "$(escape_json_data "${intra_user_key}")",
  "intra_pass_key": "$(escape_json_data "${intra_pass_key}")",
  "github_username": "$(escape_json_data "${github_username}")",
  "github_profile_link": "$(escape_json_data "github.com/${github_username}")"
}
EOF

input_auth_data() {
  printf '*> Author: '
  read -r author_name
  printf '*> Holberton Username: '
  read -r intra_user_key
  printf '*> Holberton Password: '
  read -r intra_pass_key
  printf '*> GitHub Username: '
  read -r github_username
}

{ tput bold
  tput sitm
  cat
  tput sgr0
} 2> /dev/null << 'EOF'
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::

.,     W
][     "
]bWW, WW  ]bWb ]bWb  dWb .dWW, dWW, WdW[ dWW,]bWb  dWb  WdW[
]P ][  W  ]P T[]P T[]P T[]bm,`]P  ` W`   `md[]P T[]bmd[ W`
][ ][  W  ][ ][][ ][][ ][ ""W,][    W   .W"T[][ ][]P""` W
][ ][.mWm,]WmW`]WmW`'WmW`]mmd['Wmm[ W   ]bmW[]WmW`'Wmm[ W
'` '`'"""`]["` ]["`  '"`  """  '""  "    ""'`]["`  '""  "
          ][   ][                            ][

:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

EOF

if test -f ${AUTH_FILE}; then
  printf 'Found existing configuration in %s\n' "'${AUTH_FILE}'"
  printf 'Overwrite? [Y/n] '
  read -r REPLY
  case "${REPLY}" in
    [Yy]*)
      printf 'Configuration will be overwritten.\m'
      input_auth_data && write_auth_data
      ;;
    *)
      printf 'Configuration will not be changed.\n'
      ;;
  esac
else
  input_auth_data && write_auth_data
fi

#if grep -q ENTER_FULL_PATHNAME_TO_DIRECTORY_HERE hipposcraper.py
#then
#  sed -i "s/ENTER_FULL_PATHNAME_TO_DIRECTORY_HERE/$(pwd)/g" hipposcraper.py
#fi
#
#echo "Setting aliases:"
#if ! grep -q hippodir ~/.bashrc || \
#  ! grep -q hippodoc ~/.bashrc || \
#  ! grep -q hipposcraper ~/.bashrc
#then
#  echo -e "\n# Hipposcraper aliases" >> ~/.bashrc
#fi
#
#if ! grep -q hippodir.py ~/.bashrc
#then
#  project_alias="alias hippodir='python3 $(pwd)/hippodir.py'"
#  echo "$project_alias" >> ~/.bashrc
#  echo "  -> $project_alias"
#else
#  echo "  -> hippodir already defined"
#fi
#
#if ! grep -q hippodoc.py ~/.bashrc
#then
#  read_alias="alias hippodoc='python3 $(pwd)/hippodoc.py'"
#  echo "$read_alias" >> ~/.bashrc
#  echo "  -> $read_alias"
#else
#  echo "  -> hippodoc already defined"
#fi
#
#if ! grep -q hipposcraper.py ~/.bashrc
#then
#  scrape_alias="alias hipposcraper='python3 $(pwd)/hipposcraper.py'"
#  echo "$scrape_alias" >> ~/.bashrc
#  echo "  -> $scrape_alias"
#else
#  echo "  -> hipposcraper already defined"
#fi
#
#echo "Reloading .bashrc:"
#. ~/.bashrc
#
#echo "All set!"
