FROM debian:stable

MAINTAINER Clifton Barnes <clifton.a.barnes@gmail.com>

RUN apt-get update
RUN apt-get install -y python python-dev python-pip python-smbus nginx uwsgi uwsgi-plugin-python
RUN pip install flask

EXPOSE 80

ADD www /var/www/rovercode/www
ADD nginx-site /etc/nginx/sites-enabled/rovercode

WORKDIR /var/www/rovercode/www/Adafruit_Python_GPIO
RUN python setup.py install
WORKDIR /var/www/rovercode/www
RUN echo '/etc/init.d/nginx start && uwsgi rovercode.ini --plugin python' > /usr/bin/run.sh
ENTRYPOINT ["bash", "/usr/bin/run.sh"]
