#! /bin/bash

INI_DIR=www/

if [ ! -e ${INI_DIR} ]; then
	echo "Error: uwsgi ini directory not found."
	exit 2
fi

pushd ${INI_DIR} > /dev/null
uwsgi rovercode.ini --plugin python
popd > /dev/null

echo "rovercode service started"
