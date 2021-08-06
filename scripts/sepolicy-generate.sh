#!/usr/bin/env bash
# usage:
#  ./sepolicy-generate.sh samplebeat /usr/share/samplebeat/bin/samplebeat [~/selinux/beats]
set -eu

APP=${APP:-${1:?}}
APP_BIN=${APP_BIN:-${2:?}}
INSTALL_PATH=${INSTALL_PATH:-${3:-${PWD}}}

mkdir -vp ${INSTALL_PATH}
cd ${INSTALL_PATH}

sepolicy generate --name ${APP} --path ${INSTALL_PATH} --init ${APP_BIN}

sed -i '/permissive ${APP}_t;/d' ${APP}.te
sed -i '/# This is an example. You will need to change it./d' ${APP}_selinux.spec
sed -i 's#http://HOSTNAME#https://localhost#g' ${APP}_selinux.spec
sed -i 's/YOUR NAME <YOUR@EMAILADDRESS>/Selinux <selinux@local>/g' ${APP}_selinux.spec
sed -i 's#+%x %X#+%m/%d/%Y %T#' ${APP}.sh
