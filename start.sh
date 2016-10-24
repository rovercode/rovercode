#! /bin/bash

INI_DIR=www/

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

if [ ! -e ${INI_DIR} ]; then
	echo "Error: uwsgi ini directory not found."
	exit 2
fi

pushd ${INI_DIR} > /dev/null
uwsgi rovercode.ini --plugin python
popd > /dev/null

echo "rovercode service started"
