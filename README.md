![actionshot](https://media.giphy.com/media/JRaXUIxBXgXU2ap3LI/giphy.gif)

![screenshot](https://i.imgur.com/oaX89pOg.png)

# Rovercode

[![Chat](https://img.shields.io/badge/chat-developer-brightgreen.svg?style=flat)](https://rovercode.zulipchat.com)
[![Zenhub Board](https://img.shields.io/badge/board-zenhub-purple.svg?style=flat)](https://app.zenhub.com/workspaces/rovercode-development-5c7e819df524621425116d03/boards)
[![](https://images.microbadger.com/badges/image/cabarnes/rovercode.svg)](https://microbadger.com/images/cabarnes/rovercode)
[![Build Status](https://travis-ci.org/rovercode/rovercode.svg?branch=development)](https://travis-ci.org/rovercode/rovercode)
[![Coverage Status](https://coveralls.io/repos/github/rovercode/rovercode/badge.svg)](https://coveralls.io/github/rovercode/rovercode)

Rovercode is easy-to-use package for controlling robots (rovers) that can sense and react to their environment. The Blockly editor makes it easy to program and run your bot straight from your browser. Just drag and drop your commands to drive motors, read values from a variety of supported sensors, and see what your rover sees with the built in webcam viewer.

Rovercode runs on a [Raspberry Pi 3](https://www.raspberrypi.org/products/raspberry-pi-3-model-b-plus/) with the [GrovePi+ sensor board](https://www.seeedstudio.com/GrovePi-p-2241.html) and the [Grove I2C motor controller board](https://www.seeedstudio.com/Grove-I2C-Motor-Driver-p-907.html).

## Setup

### Creating Your .env
First, create an app.rovercode.com account [here](https://app.rovercode.com/accounts/login).
Then, navigate to the "My Rovers" section and create a new rover.
Once it is created, click the "Download Credentials" button at the bottom of the rover's detail page.
The file will download as something like `rovercode_yourrovername.env`.
Save this file to a flash drive.

### Rover Setup
First, on your Raspberry Pi:
```bash
# Install Docker and other helpers
$ sudo apt install git docker.io
$ mkdir -p /lib/systemd/system/rovercode /opt/rovercode/
# Put the service definitions in the systemd folder
$ git clone https://github.com/rovercode/rovercode.git && cd rovercode
$ cp services/* /lib/systemd/system/rovercode/
$ cp scripts/* /opt/rovercode/
# Turn off your Raspberry Pi, insert your thumbdrive with the `rovercode_yourrovername.env` file, and turn the Raspberry Pi back on.
```
Once the Raspberry Pi restarts, the comissioning service should run, followed by the rovercode service.
Run `sudo systemctl status rovercode.service` to confirm that it is running.
Then, on any PC or tablet, head to app.rovercode.com to connect to your rover.

### Development PC Setup
When developing Rovercode, you may want to run Rovercode on your PC instead of a Raspberry Pi.
Below are instructions for how to install and run Rovercode on your PC.

```bash
$ git clone --recursive https://github.com/rovercode/rovercode.git && cd rovercode
$ sudo docker build -t rovercode .
# Copy in the `rovercode_yourrovername.env` file as `.env` (nothing before the dot)
$ cp ~/Downloads/rovercode_yourrovername.env .env
$ docker run --env DEVELOPMENT=true --name rovercode -v $PWD:/var/rovercode rovercode
```
Note the `--env DEVELOPMENT=true` flag.
Then, still on your development PC, head to app.rovercode.com and connect to your "rover" (your PC running the service).

## Testing
Run the tests like this:
Make sure the container is running (the `sudo docker run ...` command above), then in another terminal, do:
```bash
$ docker exec rovercode python -m pytest
$ docker exec rovercode prospector

```

## Docs
More detailed usage instructions can be found [here](https://contributor-docs.rovercode.com/rovercode/development/index.html).

Read the complete docs [here](https://contributor-docs.rovercode.com).

## Contact

We'd love to say hi! Join [our chat!](https://rovercode.zulipchat.com).

## License
[GNU GPLv3](license) © Rovercode LLC and Rovercode contributors
