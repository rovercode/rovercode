#! /bin/bash

ADAFRUIT_DIR=www/Adafruit_Python_GPIO

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

if [ ! -e ${ADAFRUIT_DIR} ]; then
	echo "Error: Adafruit directory not found."
	exit 2
fi

apt-get install -y python python-dev python-pip python-smbus nginx
pip install flask uwsgi

pushd ${ADAFRUIT_DIR} > /dev/null
python setup.py install
popd > /dev/null

sed "s@__ROOTDIR__@$(pwd)@" nginx-site > rovercode-nginx-site
ln -s $(pwd)/rovercode-nginx-site /etc/nginx/sites-enabled/rovercode
service nginx restart

echo "Setup complete."

exit 0
