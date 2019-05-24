![screenshot](https://i.imgur.com/BSzTTkF.png)

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
First, create a rovercode.com account [here](https://rovercode.com/accounts/signup/). Then, navigate to the "My Rovers" section and
create a new rover. Once it is created, click the "Download Credentials" button at the bottom of the rover's detail page. The file
will download as something like `rovercode_yourrovername.env`. Rename the file as only `.env` (nothing before the dot) and save it in the same directory as this README.

### Rover Setup
First, on your Rover (Raspberry Pi):
```bash
$ # create your .env, as described in the section below
$ sudo apt install git
$ git clone --recursive https://github.com/rovercode/rovercode.git && cd rovercode
$ sudo bash setup.sh #run this only once -- it will take some time
$ sudo bash start.sh #run this each time you boot the rover (or automatically start if chosen in setup)
```
Then, on any PC or tablet, head to rovercode.com to connect to your rover.

### Development PC Setup
When developing Rovercode, you may want to run Rovercode on your PC instead of a Raspberry Pi. Below are instructions for how to install and run rovercode on your PC. Everything should work fine: rovercode will automatically detect that it is not running on target hardware and will stub out the calls to the motors and sensors.

```bash
$ # create your .env, as described in the section below
$ sudo apt install git docker.io
$ git clone https://github.com/rovercode/rovercode.git && cd rovercode
$ sudo docker build -t rovercode .
$ sudo docker run --env DEVELOPMENT=true --name rovercode -v $PWD:/var/rovercode rovercode

```
Then, still on your development PC, head to rovercode.com and connect to your "rover" (your PC running the service).

## Testing
Run the tests like this:
Make sure the container is running (the `sudo docker run ...` command above), then in another terminal, do:
```bash
$ sudo docker exec -it rovercode bash -c "DEVELOPMENT=true python -m pytest"
$ sudo docker exec -it rovercode bash -c prospector

```

## Docs
More detailed usage instructions can be found [here](https://contributor-docs.rovercode.com/rovercode/development/index.html).

Read the complete docs [here](https://contributor-docs.rovercode.com).

## Contact

We'd love to chat with you! Join the [our chat!](https://rovercode.zulipchat.com).

## License
[GNU GPLv3](license) © Rovercode LLC and Rovercode contributors
