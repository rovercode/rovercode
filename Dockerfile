FROM python:3.6-slim-stretch

MAINTAINER Clifton Barnes <clifton.barnes@rovercode.com>

COPY pytest.ini requirements.txt /var/rovercode/
COPY GrovePi /var/rovercode/GrovePi
COPY rovercode /var/rovercode/rovercode
COPY commissioning /var/rovercode/commissioning

WORKDIR /var/rovercode
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libi2c-dev \
    python3-smbus \
&& pip install -r requirements.txt \
&& apt-get remove -y --purge --auto-remove build-essential \
&& rm -rf /var/lib/apt/lists/*

WORKDIR /var/rovercode/GrovePi/Software/Python
RUN python setup.py install

WORKDIR /var/rovercode/rovercode

CMD ["python", "app.py"]
