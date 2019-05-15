#! /bin/bash

LOCATION="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

echo "rovercode service starting"
python3.6 ${LOCATION}/${APP_DIR}app.py
docker run --name rovercode --privileged -v /dev:/dev -v ${LOCATION}:/var/rovercode rovercode
echo "rovercode service stopped"
