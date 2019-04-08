FROM python:3.6-slim-stretch

MAINTAINER Clifton Barnes <clifton.barnes@rovercode.com>

RUN apt-get update
RUN apt-get install -y build-essential python3-dev libi2c-dev python3-smbus

ADD .env /var/rovercode/.env
ADD pytest.ini /var/rovercode/pytest.ini
ADD requirements.txt /var/rovercode/requirements.txt
ADD GrovePi /var/rovercode/GrovePi
ADD rovercode /var/rovercode/rovercode

WORKDIR /var/rovercode
RUN pip install -r requirements.txt

WORKDIR /var/rovercode/GrovePi/Software/Python
RUN python setup.py install
WORKDIR /var/rovercode/rovercode
RUN echo 'python3.6 app.py' > /usr/bin/run.sh
ENTRYPOINT ["bash", "/usr/bin/run.sh"]
