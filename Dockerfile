FROM debian:stable

MAINTAINER Clifton Barnes <clifton.a.barnes@gmail.com>

RUN apt-get update
RUN apt-get install -y python python-dev python-pip lighttpd
RUN pip install flask flask_cors

EXPOSE 80 5000

ADD www /var/www/html/

WORKDIR /var/www/html
RUN echo '/etc/init.d/lighttpd start && python /var/www/html/app.py' > /usr/bin/run.sh
ENTRYPOINT ["bash", "/usr/bin/run.sh"]
