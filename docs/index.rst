.. Rovercode documentation master file, created by
   sphinx-quickstart on Mon Dec 26 16:06:49 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rovercode
============
:License: GPLv3
:Source: `<https://github.com/rovercode/rovercode>`_
:Hosted at: `<https://rovercode.com>`_ (master) and `<https://beta.rovercode.com>`_ (development)

.. image:: https://img.shields.io/badge/chat-developer-brightgreen.svg?style=flat
      :target: http://rovercode.zulip.com/
.. image:: https://api.travis-ci.org/rovercode/rovercode.svg
      :target: https://travis-ci.org/rovercode/rovercode
.. image:: https://coveralls.io/repos/github/rovercode/rovercode/badge.svg?branch=development
      :target: https://coveralls.io/github/rovercode/rovercode?branch=deveopment

Welcome!
#########

rovercode is an easy-to-use system for controlling robots (rovers) that can sense and react to their environment.
The Blockly editor makes it easy to program and run your bot straight from your
browser. Just drag and drop your commands to drive motors, read values from a
variety of supported sensors, and see what your rover sees with the built
in webcam viewer.

.. image:: https://rovercode.com/static/images/screenshot.jpg

Architecture
#############

rovercode is made up of two parts:

- rovercode (the docs you're reading right now) is the service that runs on the rover.
- rovercode-web (a separate repo `documented here <http://rovercode-web.readthedocs.io/>`_) is the web app running at `rovercode.com <https://rovercode.com>`_.

Rovercode runs on a Raspberry Pi 3 with the [GrovePi+ sensor board](https://www.seeedstudio.com/GrovePi-p-2241.html) and the [Grove I2C motor controller board](https://www.seeedstudio.com/Grove-I2C-Motor-Driver-p-907.html).

Get Started
############
Check out the `quickstart guide <quickstart.html>`_. Then see `how to
contribute <contribute.html>`_.

Contact
########
Also, we'd love to chat with you! Join `our chat
<http://rovercode.zulipchat.com>`_.


Contents
########

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   quickstart
   detailed-usage
   contribute
   api
   build-a-rover
   websocket-protocol
   example-rover-config


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
