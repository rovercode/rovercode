.. Rovercode documentation master file, created by
   sphinx-quickstart on Mon Dec 26 16:06:49 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

rovercode
============

Welcome! rovercode is made up of two parts:

- rovercode (the docs you're reading right now) is the service that runs on the rover.
- rovercode-web (a separate repo `documented here <http://rovercode-web.readthedocs.io/>`_) is the web app running at `rovercode.com <https://rovercode.com>`_.

rovercode and rovercode-web work together to make an an easy-to-use system
for controlling robots (rovers) that can sense and react to their environment.
The Blockly editor makes it easy to program and run your bot straight from your
browser. Just drag and drop your commands to drive motors, read values from a
variety of supported sensors, and see what your rover sees with the built
in webcam viewer.

The rovercode service (this documentation) runs on the rover. The rover can be
any single-board-computer supported by the Adafruit Python GPIO wrapper library,
including the NextThingCo CHIP, Raspberry Pi, and BeagleBone Black.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   quickstart
   api

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
