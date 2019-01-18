FROM python:3.6-jessie

MAINTAINER Clifton Barnes <clifton.barnes@rovercode.com>

RUN apt-get update
RUN apt-get install -y python3-dev libi2c-dev

# https://www.linuxcircle.com/2015/05/03/how-to-install-smbus-i2c-module-for-python-3/
# TODO: Remove this build once python3-smbus is not needed
WORKDIR /tmp
RUN wget http://ftp.de.debian.org/debian/pool/main/i/i2c-tools/i2c-tools_3.1.0.orig.tar.bz2
RUN tar xavf i2c-tools_3.1.0.orig.tar.bz2
WORKDIR /tmp/i2c-tools-3.1.0/py-smbus
RUN mv smbusmodule.c smbusmodule.c.orig
RUN wget https://gist.githubusercontent.com/sebastianludwig/c648a9e06c0dc2264fbd/raw/2b74f9e72bbdffe298ce02214be8ea1c20aa290f/smbusmodule.c
RUN python3 setup.py build
RUN python3 setup.py install

ADD .env /var/rovercode/.env
ADD conftest.py /var/rovercode/conftest.py
ADD requirements.txt /var/rovercode/requirements.txt
ADD Adafruit_Python_GPIO /var/rovercode/Adafruit_Python_GPIO
ADD rovercode /var/rovercode/rovercode

WORKDIR /var/rovercode
RUN pip install -r requirements.txt

WORKDIR /var/rovercode/Adafruit_Python_GPIO
RUN python setup.py install
WORKDIR /var/rovercode/rovercode
RUN echo 'python3.6 app.py' > /usr/bin/run.sh
ENTRYPOINT ["bash", "/usr/bin/run.sh"]
