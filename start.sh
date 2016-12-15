#! /bin/bash

INI_DIR=www/
UWSGI_EXEC=uwsgi

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

if [ ! -e ${INI_DIR} ]; then
	echo "Error: uwsgi ini directory not found."
	exit 2
fi

pushd ${INI_DIR} > /dev/null
echo "rovercode service starting"
if [ ! -e ${UWSGI_EXEC} ]; then
	echo "Error: could not find uwsgi binary. Did you run start.sh?"
	exit 2
fi
./uwsgi rovercode.ini --plugins python,corerouter,http,gevent --gevent 1000 --http-websockets
popd > /dev/null
echo "rovercode service stopped"
