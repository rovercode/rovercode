quickstart
===========

Standard Setup (on rover)
##########################
First, on your rover (CHIP, Raspberry Pi, BeagleBone, etc):

.. code-block:: guess

    $ sudo apt install git
    $ git clone --recursive https://github.com/aninternetof/rovercode.git && cd rovercode
    $ sudo bash setup.sh #run this only once -- it will take some time
    $ sudo bash start.sh #run this each time you boot the rover (or automatically start if chosen in setup)

Then, on any PC or tablet, head to rovercode.com to connect to your rover. Start playing!

Development Setup (on development PC)
#####################################
When developing rovercode, you may want to run rovercode on your PC instead of a CHIP/Raspberry Pi/Beaglebone. Below are instructions for how to install and run rovercode on your PC. Everything should work fine: rovercode will automatically detect that it is not running on target hardware and will stub out the calls to the motors and sensors.

First, on your development PC:

.. code-block:: guess

    $ sudo apt install git
    $ git clone --recursive https://github.com/aninternetof/rovercode.git && cd rovercode
    $ sudo bash setup.sh #run this only once -- it will take some time
    $ sudo bash start.sh #run this each time

Then, still on your development PC, head to rovercode.com and connect to your "rover" (your PC running the service).

Alternate Development Setup (on development PC using Docker)
#############################################################
Rather use Docker? First, on your development PC:

.. code-block:: guess

    $ sudo apt install git docker.io
    $ git clone --recursive https://github.com/aninternetof/rovercode.git && cd rovercode
    $ sudo docker build -t rovercode .
    $ sudo docker run --name rovercode -v $PWD:/var/www/rovercode -p 80:80 -d rovercode

Then, still on your development PC, head to rovercode.com and connect to your "rover" (your PC running the service).
