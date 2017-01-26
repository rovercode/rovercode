#! /bin/bash

INI_DIR=www/
ADAFRUIT_DIR=www/Adafruit_Python_GPIO
UWSGI_DIR=uwsgi/

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

if [ ! -e ${ADAFRUIT_DIR} ]; then
	echo "Error: Adafruit directory not found."
	exit 2
fi

apt-get install -y python python-dev python-pip python-smbus nginx build-essential git libssl-dev
pip install flask flask-socketio gevent uwsgi Sphinx==1.4.8 sphinx_rtd_theme

pushd ${ADAFRUIT_DIR} > /dev/null
python setup.py install
popd > /dev/null

git clone -b uwsgi-2.0 https://github.com/unbit/uwsgi.git
pushd ${UWSGI_DIR} > /dev/null
python uwsgiconfig.py --build core
python uwsgiconfig.py --plugin plugins/python core
python uwsgiconfig.py --plugin plugins/corerouter core
python uwsgiconfig.py --plugin plugins/http core
python uwsgiconfig.py --plugin plugins/gevent core
popd > /dev/null

cp ${UWSGI_DIR}/uwsgi ${INI_DIR}
cp ${UWSGI_DIR}/python_plugin.so ${INI_DIR}
cp ${UWSGI_DIR}/corerouter_plugin.so ${INI_DIR}
cp ${UWSGI_DIR}/http_plugin.so ${INI_DIR}
cp ${UWSGI_DIR}/gevent_plugin.so ${INI_DIR}
rm -rf ${UWSGI_DIR}

rm -rf /var/www/rovercode > /dev/null
mkdir -p /var/www/rovercode
ln -s $(pwd)/www /var/www/rovercode/www
ln -fs $(pwd)/nginx-site /etc/nginx/sites-enabled/rovercode
rm -rf /etc/nginx/sites-enabled/default > /dev/null
service nginx restart

echo "Setup complete."

exit 0
