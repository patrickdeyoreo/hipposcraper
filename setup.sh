#!/usr/bin/env sh
# Install and configure the hipposcraper.

PACKAGE='hipposcraper'
PROGRAM='hipposcraper.py'

SRC_DIR="$(CDPATH='' cd -- "${0%/*}" && pwd -P)"

PKG_SRC="${SRC_DIR}/${PACKAGE}"
PRG_SRC="${SRC_DIR}/${PROGRAM}"

HIPPO_HOME="${HIPPO_HOME:-${XDG_DATA_HOME:-${HOME}/.local/share}/hipposcraper}"
HIPPO_AUTH="${HIPPO_HOME}/credentials.json"


main() {
  check_privilege
  show_off_banner
  echo
  install_depends
  echo
  make_hippo_home
  echo
  install_package
  echo
  configure_login
  echo
  update_shell_rc
}


check_privilege() {
  if test "$(id -u)" -eq 0; then
    2>&1 printf '%s: refusing to run as root\n' "$0"
    exit 1
  fi
}


show_off_banner() {
  tput bold
  cat
  tput sgr0
  sleep 1
} 2> /dev/null << 'EOF'

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#     #
#     # # #####  #####   ####   ####   ####  #####    ##   #####  ###### #####
#     # # #    # #    # #    # #      #    # #    #  #  #  #    # #      #    #
####### # #    # #    # #    #  ####  #      #    # #    # #    # #####  #    #
#     # # #####  #####  #    #      # #      #####  ###### #####  #      #####
#     # # #      #      #    # #    # #    # #   #  #    # #      #      #   #
#     # # #      #       ####   ####   ####  #    # #    # #      ###### #    #
:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

EOF


install_depends() {
  if ! python3 -m pip install --user -U -r "${SRC_DIR}/requirements.txt"; then
    2>&1 printf '%s: failed to install dependencies\n' "$0"
    exit 1
  fi
}


make_hippo_home() {
  if ! test -d "${HIPPO_HOME}"; then
    if ! rm -fv -- "${HIPPO_HOME}"; then
      2>&1 printf '%s: %s: failed to remove file\n' "$0" "${HIPPO_HOME}"
      exit 1
    fi
    if ! mkdir -v -- "${HIPPO_HOME}"; then
      2>&1 printf '%s: %s: failed to create directory\n' "$0" "${HIPPO_HOME}"
      exit 1
    fi
  fi
  if ! chown -c "$(id -u)" -- "${HIPPO_HOME}"; then
      2>&1 printf '%s: %s: failed to set file owner\n' "$0" "${HIPPO_HOME}"
      exit 1
  fi
  if ! chmod -c u+rwx -- "${HIPPO_HOME}"; then
      2>&1 printf '%s: %s: failed to set file mode\n' "$0" "${HIPPO_HOME}"
      exit 1
  fi
}


escape_json_str() {
  printf '%s' "$1" | sed 's:["\]:\\&:g'
}


save_login_data() {
  cat > "${HIPPO_AUTH}"
} << EOF
{
  "author_name": "$(escape_json_str "${author_name}")",
  "intra_user_key": "$(escape_json_str "${intra_user_key}")",
  "intra_pass_key": "$(escape_json_str "${intra_pass_key}")",
  "github_username": "$(escape_json_str "${github_username}")",
  "github_profile_link": "$(escape_json_str "github.com/${github_username}")"
}
EOF


install_package() {
  printf 'Copying %s into %s ...\n' "${PKG_SRC}" "${HIPPO_HOME}'"
  cp -a -- "${PKG_SRC}" "${PRG_SRC}" "${HIPPO_HOME}"
}


read_login_data() {
  printf '*> Author: '
  read -r author_name
  printf '*> Holberton Username: '
  read -r intra_user_key
  printf '*> Holberton Password: '
  read -r intra_pass_key
  printf '*> GitHub Username: '
  read -r github_username
}


configure_login() {
  if test -f "${HIPPO_AUTH}"; then
    printf 'Found existing configuration in %s\n' "'${HIPPO_AUTH}'"
    printf 'Overwrite? [Y/n] '
    read -r REPLY
    case "${REPLY}" in
      [Yy]*)
        printf 'Configuration will be overwritten.\n'
        ;;
      *)
        printf 'Configuration will not be changed.\n'
        return 0
        ;;
    esac
  fi
  if read_login_data && save_login_data; then
    printf 'Configuration written to %s\n' "${HIPPO_AUTH}"
  else
    printf 'Failed to write configuration to %s\n' "${HIPPO_AUTH}"
  fi
}


update_shell_rc() {
  cat
} << EOF
To complete installation, the execution environment needs to be updated.
You may add the following to a shell init script (e.g. ~/.bashrc, etc.):

export HIPPO_HOME="${HIPPO_HOME}"
export PATH="\${PATH:+\${PATH}:}\${HIPPO_HOME}"

If you prefer to manage the environment some other way, modify as needed.

Once the configuration is complete, open a shell and run 'hipposcraper.py'
EOF


main "$@"


# vim:et:sts=2:sw=2
