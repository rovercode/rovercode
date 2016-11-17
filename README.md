![screenshot](http://rovercode.org/img/screenshot.jpg)

# rovercode

[![Gitter](https://badges.gitter.im/aninternetof/rovercode.svg)](https://gitter.im/aninternetof/rovercode?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![MailingList](https://img.shields.io/badge/join-mailing%20list-yellow.svg?style=flat)](http://rovercode.org/cgi-bin/mailman/listinfo/developers)
[![](https://images.microbadger.com/badges/image/cabarnes/rovercode.svg)](https://microbadger.com/images/cabarnes/rovercode)

rovercode is easy-to-use package for controlling robots (rovers) that can sense and react to their environment. The Blockly editor makes it easy to program and run your bot straight from your browser. Just drag and drop your commands to drive motors, read values from a variety of supported sensors, and see what your rover sees with the built in webcam viewer.

rovercode runs on any single-board-computer supported by the [Adafruit Python GPIO wrapper library](https://github.com/adafruit/Adafruit_Python_GPIO), including the NextThingCo CHIP, Raspberry Pi, and BeagleBone Black. Once installed, just point your browser at the rover's address and get started.

[Try a live demo.](http://codetherover.com/demo/rover-code/www/mission-control.html)

## Setup

### Standard Setup
First, on your rover (CHIP, Raspberry Pi, BeagleBone, etc):
```bash
$ sudo apt install git
$ git clone --recursive https://github.com/aninternetof/rovercode.git && cd rovercode
$ sudo ./setup.sh #run this only once -- it will take some time
$ sudo ./start.sh #run this each time you boot the rover
```
Then, on any PC or tablet, point your browser to your robot's IP address. You're done! Start playing!

### Development PC Setup
When developing rovercode, you may want to run rovercode on your PC instead of a CHIP/Raspberry Pi/Beaglebone. Below are instructions for how to install and run rovercode on your PC. Everything should work fine: rovercode will automatically detect that it is not running on target hardware and will stub out the calls to the motors and sensors.

#### Development PC Standard Setup
First, on your development PC:
```bash
$ sudo apt install git
$ git clone --recursive https://github.com/aninternetof/rovercode.git && cd rovercode
$ sudo ./setup.sh #run this only once -- it will take some time
$ sudo ./start.sh #run this each time you want to work on rovercode
```
Then, still on your development PC, point your browser to `localhost`.

#### Development PC Alternate Setup (Docker)
Rather use Docker? Sure! First, on your development PC:
```bash
$ sudo apt install git docker.io
$ git clone --recursive https://github.com/aninternetof/rovercode.git && cd rovercode
$ sudo docker build -t rovercode ./ #run this only once -- it will take some time
$ sudo docker run -p 80:80 rovercode #run this each time you want to work on rovercode

```
Then, still on your development PC, point your browser to `localhost`.

## Play and Contribute
rovercode is usable now, but we have lots of great features left to be added. Check out the [contributing instructions](https://github.com/aninternetof/rovercode/wiki/Contributing) then head over to the [feature tracker](https://huboard.com/aninternetof/rovercode) to see if there's something fun to contribute.

## License
[GNU GPLv3](license) © Brady L. Hurlburt and the rovercode.org community
