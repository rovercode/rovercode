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
rovercode allows you to control a robot, sense the robot's enivornment, and watch from an onboard camera.

rovercode is a webservice that you host from your robot. Currently, it can run on NextThingCo CHIP, Raspberry Pi, and BeagleBone Black (basically anything supported by the [Adafruit Python GPIO wrapper library](https://github.com/adafruit/Adafruit_Python_GPIO)).

In your browser, you design the code using [Blockly](https://developers.google.com/blockly/). Then, your browser interprets it into Javascript and executes it (in a sandbox of course). Motor commands are sent from your browswer to the robot, and real-time sensor information is sent from the robot to the browser.

[Try a live demo](http://codetherover.com/demo/rover-code/www/mission-control.html)

## Install, Play and Contribute
rovercode is on its first release. It is usable now, but we have lots of great features left to be added. Check out the [install instructions](https://github.com/aninternetof/rovercode/wiki/Getting-Set-Up) and the [contributing instructions](https://github.com/aninternetof/rovercode/wiki/Contributing). Check out the [feature tracker](https://github.com/aninternetof/rovercode/issues?utf8=%E2%9C%93&q=is%3Aissue%20is%3Aopen%20label%3Afeature) to see if there's something fun to contribute.

## Licence
[GNU GPLv3](license) © Brady L. Hurlburt and the rovercode.org community
