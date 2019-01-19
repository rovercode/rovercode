#! /bin/bash

INI_DIR=rovercode/
ADAFRUIT_DIR=Adafruit_Python_GPIO
GROVEPI_DIR=GrovePi

if [ "${EUID}" -ne 0 ]; then
	echo "Error: This script must be run as root."
	exit 1
fi

if [ ! -e ${ADAFRUIT_DIR} ]; then
	echo "Error: Adafruit directory not found."
	exit 2
fi

if [ ! -e ${GROVEPI_DIR} ]; then
	echo "Error: GrovePi directory not found."
	exit 2
fi

apt-get install -y python3 python3-dev python3-pip libi2c-dev

# https://www.linuxcircle.com/2015/05/03/how-to-install-smbus-i2c-module-for-python-3/
# TODO: Remove this build once python3-smbus is not needed
apt-get install python3-dev
apt-get install libi2c-dev
pushd /tmp > /dev/null
wget http://ftp.de.debian.org/debian/pool/main/i/i2c-tools/i2c-tools_3.1.0.orig.tar.bz2 # download Python 2 source
tar xavf i2c-tools_3.1.0.orig.tar.bz2
cd i2c-tools-3.1.0/py-smbus
mv smbusmodule.c smbusmodule.c.orig # backup
wget https://gist.githubusercontent.com/sebastianludwig/c648a9e06c0dc2264fbd/raw/2b74f9e72bbdffe298ce02214be8ea1c20aa290f/smbusmodule.c # download patched (Python 3) source
python3 setup.py build
python3 setup.py install
popd > /dev/null

pip install virtualenv && \
virtualenv --system-site-packages env && \
. env/bin/activate && \
pip install -r requirements.txt

pushd ${ADAFRUIT_DIR} > /dev/null
python setup.py install
popd > /dev/null

pushd ${GROVEPI_DIR}/Software/Python > /dev/null
python setup.py install
popd > /dev/null

# Ask the user if they want to start automatically on boot
ask() {
    # http://djm.me/ask
    local prompt default REPLY

    while true; do

        if [ "${2:-}" = "Y" ]; then
            prompt="Y/n"
            default=Y
        elif [ "${2:-}" = "N" ]; then
            prompt="y/N"
            default=N
        else
            prompt="y/n"
            default=
        fi

        # Ask the question (not using "read -p" as it uses stderr not stdout)
        echo -n "$1 [$prompt] "

        # Read the answer (use /dev/tty in case stdin is redirected from somewhere else)
        read REPLY </dev/tty

        # Default?
        if [ -z "$REPLY" ]; then
            REPLY=$default
        fi

        # Check if the reply is valid
        case "$REPLY" in
            Y*|y*) return 0 ;;
            N*|n*) return 1 ;;
        esac

    done
}

if ask "Do you want to automatically start on boot? (choose N for development):"; then
    echo "Going to start on boot..."
    mkdir .backup && cp /etc/rc.local .backup/
    sed -i -e '$i \bash '$(pwd)'\/start.sh \&\n' /etc/rc.local
else
    echo "Not going to start on boot..."
fi

echo "Setup complete."

exit 0
