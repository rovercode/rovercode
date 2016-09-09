![screenshot](http://rovercode.org/img/screenshot.jpg)

# rovercode

[![Gitter](https://badges.gitter.im/aninternetof/rovercode.svg)](https://gitter.im/aninternetof/rovercode?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)
[![MailingList](https://img.shields.io/badge/join-mailing%20list-yellow.svg?style=flat)](http://rovercode.org/cgi-bin/mailman/listinfo/developers)

## Setup
First, on your robot:
```
$ git clone https://git.io/rovercode.git
```
Then, on your PC or tablet, point your browser to your robot's IP address.

*A very nice install.sh is is coming soon. For now, use the [install instructions](https://github.com/aninternetof/rovercode/wiki/Getting-Set-Up) to set up dependencies.*

## Description
rovercode is a webservice that you host from your single-board-computer robot. The webservice hosts a webpage in which you design your code, and then it interfaces with the motors and sensors on your robot to execute your code. Currently, it can run on NextThingCo CHIP, Raspberry Pi, and BeagleBone Black (basically anything supported by the [Adafruit Python GPIO wrapper library](https://github.com/adafruit/Adafruit_Python_GPIO)).

In your browser, you design the code for your robot to execute using [Blockly](https://developers.google.com/blockly/). Then, your browser interprets it into Javascript and executes it in a sandbox. Motor commands are sent to the server (host/robot/single-board computer). Sensor information is sent from the server (host/robot/single-board computer) to the browser.

Finally, there's a webcam feed for a live view from your robot.

## Install, Play and Contribute
rovercode is on its first release. It is usable now, but we have lots of great features left to be added. Check out the [install instructions](https://github.com/aninternetof/rovercode/wiki/Getting-Set-Up) and the [contributing instructions](https://github.com/aninternetof/rovercode/wiki/Contributing). Check out the [feature tracker](https://github.com/aninternetof/rovercode/issues) to see if there's something fun to contribute.

## Licence
[GNU GPL V3](license) © Brady L. Hurlburt and the rovercode.org community
