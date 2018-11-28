#! /bin/bash

LOCATION="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"
APP_DIR=www/

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

source ${LOCATION}/env/bin/activate && \

pushd ${LOCATION}/${APP_DIR} > /dev/null
echo "rovercode service starting"
python ${LOCATION}/${APP_DIR}app.py
popd > /dev/null
echo "rovercode service stopped"
