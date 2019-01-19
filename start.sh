#! /bin/bash

APP_DIR=rovercode/

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

. env/bin/activate && \

pushd ${APP_DIR} > /dev/null
echo "rovercode service starting"
python3.6 app.py
popd > /dev/null
echo "rovercode service stopped"
