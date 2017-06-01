build a rover
===============

future plans
-------------
We are developing a rover reference design that includes a `custom daughter
board <https://upverter.com/ductape/084de978df61d3cb/rovercode/>`_, a Lexan
chassis, and `MEMS IR sensors
<https://upverter.com/ductape/aef33f7c39fd29d5/rovercode-prox-sensor/>`_. Join
the #hardware channel of `our Slack <http://chat.rovercode.com>`_ to
follow our progress and suggest ideas.

In the meantime, you can still build a rover like the one we built as our
first prototype. In that approach, you borrow the chassis, motors, and motor
driver circuitry from an easily-hackable RC car! Instructions for doing so
are below.

supply list
---------------
- `Thunder Tumbler RC car <https://www.amazon.com/s?ie=UTF8&field-keywords=thunder%20tumbler&index=blended&link_code=qs&tag=wwwcanoniccom-20https://www.amazon.com/s?ie=UTF8&field-keywords=thunder%20tumbler&index=blended&link_code=qs&tag=wwwcanoniccom-20>`_ (or at CVS)
- `IR emitter receiver pairs <https://www.amazon.com/gp/product/B00XPSIT3O/ref=oh_aui_search_detailpage?ie=UTF8&psc=1>`_
- `jumpers <https://www.amazon.com/SUNKEE-100pcs-female-jumper-Dupont/dp/B00AYCON8Y/ref=sr_1_3?ie=UTF8&qid=1495206374&sr=8-3&keywords=female+jumper+wire>`_
- `assorted resistors <https://www.amazon.com/E-Projects-EPC-103-Value-Resistor-Kit/dp/B00E9YQQSS/ref=sr_1_1?ie=UTF8&qid=1495206019&sr=8-1&keywords=assorted+resistors>`_
- two `small proto boards <https://www.amazon.com/Vktech-Prototype-Universal-Printed-Circuit/dp/B00CGV6TZG/ref=sr_1_14?ie=UTF8&qid=1495206282&sr=8-14&keywords=protoboard&th=1>`_
- `0.1-inch headers, male, vertical <https://www.amazon.com/Straight-Single-Header-Arduino-Prototype/dp/B01EFKXXJA/ref=sr_1_5?ie=UTF8&qid=1495206200&sr=8-5&keywords=0.1%22+male+header>`_ (we'll cut to desired length)
- `C.H.I.P <https://getchip.com/pages/chip>`_
- `webcam <https://smile.amazon.com/gp/product/B004FHO5Y6/ref=oh_aui_search_detailpage?ie=UTF8&psc=1>`_
- `powered USB hub <https://smile.amazon.com/gp/product/B00ZYKL6UO/ref=oh_aui_search_detailpage?ie=UTF8&psc=1>`_
- `USB battery <https://smile.amazon.com/gp/product/B011DD6Z2O/ref=oh_aui_search_detailpage?ie=UTF8&psc=1>`_
- soldering iron and solder

chassis, motors, wheels -- the Thunder Tumbler
-----------------------------------------------
We'll use the chassis, motors, and wheels from the venerable Thunder Tumbler
RC car. I get mine at Walgreens or CVS; sometimes they are called something
else there, but whatever RC car they sell is likely to be pretty much a
Thunder Tumbler. You can also `order one from Amazon
<https://www.amazon.com/s?ie=UTF8&field-keywords=thunder%20tumbler&index=blended&link_code=qs&tag=wwwcanoniccom-20https://www.amazon.com/s?ie=UTF8&field-keywords=thunder%20tumbler&index=blended&link_code=qs&tag=wwwcanoniccom-20>`_.

We've chosen this RC car because it's easy to hack. Specifically, it's easy
to rip out the radio controller IC. This is the IC that receives
messages from the wireless controller and drives the motors.
We don't care about the wireless controller; instead, we'd like the C.H.I.P to
drive the motors. So, we'll remove the radio controller IC, leaving empty its
pads that connected it to the motors. Then we'll connect some
GPIO from our C.H.I.P to those pads.

Preparing the Thunder Tumbler
++++++++++++++++++++++++++++++
`Here are the instructions for preparing the Thunder Tumbler
<http://www.instructables.com/id/Robot-Platform-including-h-bridges-from-10-RC-Ca/>`_.
Your end goal is to bring out these connections to a 5-pin header:

- Left motor forward
- Left motor backward
- Right motor forward
- Right motor backward
- Ground

Hot-glue this header somewhere convenient on the chassis. Later we'll run jumpers
to it from the C.H.I.P.

Here are some tweaks/tips to augment the tutorial:

- Everywhere he says "Arduino", replace it with "C.H.I.P."
- Depending on what version of the Thunder Tumbler you happen to get, the radio controller IC could be through-hole or surface-mount. If it's surface mount, try your best not to rip off the pads when you remove the IC.
- To figure out which pads are the variable left/right forward/backward motor pads, I recommend connecting a wire to the 3.3V supply on your C.H.I.P, then poking the other end around on all the pads. Observe which wheel turns and in which direction, and write it down!
- You can get ground from anywhere you want; you don't need to use a pad from the radio control IC. Use a multimeter to find a spot that reads zero resistance with the negative terminal of the RC car's battery holder.

Connecting to the C.H.I.P
++++++++++++++++++++++++++

Use your jumpers to connect the signals on your new 5-pin header to the C.H.I.P.
Ground connects to ground, and the motor control signals can connect to any
`XIO-P[0-7]` pin. Right now the pins are hard-coded in `blockly-api.js <https://github.com/aninternetof/rovercode-web/blob/development/mission_control/static/js/blockly-api.js#L3>`_
(booooo, I know), so to avoid having to edit the code, use these pins:

+-------------------+-------------+
| Motor Signal      | C.H.I.P Pin |
+===================+=============+
| left, forward     | XIO-P0      |
+-------------------+-------------+
| left, backward    | XIO-P1      |
+-------------------+-------------+
| right, forward    | XIO-P6      |
+-------------------+-------------+
| right, backward   | XIO-P7      |
+-------------------+-------------+
| ground            | any ground  |
+-------------------+-------------+


infrared sensors -- the ears
-----------------------------

We call the infrared sensors the ears of the rover. They might
be better called eyes since they operate using light (albeit
invisible light). But, the rover already has an eye (the webcam),
and the IR sensor boards stick off the the sides like ears,
so we go with it.

Building the circuit
+++++++++++++++++++++++

The rover has two ears: two IR sensor boards. They are identical.
Each has an IR transmitter and an IR receiver. This is the circuit;
create it on two of your proto boards:

.. image:: http://i.imgur.com/HpGsVQv.png

Each ear has a header with three things on it:

- 3.3V
- ground
- signal (this is what varies to indicate something is detected)

We just want a binary signal out of the sensors, so even though we have a
continuous analog signal coming out of the sensor, we won't hook it up to
an analog input of the C.H.I.P. We'll just hook it up to a regular GPIO input,
and let the input hardware of the pin serve as a rough comparator.

Just like the motor signal pins, the pins for the IR ear signals are hardcoded
at the moment (this time in `app.py <https://github.com/aninternetof/rovercode/blob/development/www/app.py#L287>`_
-- we are really gonna make this configurable soon). So to avoid having to
change code, connect this like this:

Connecting to the C.H.I.P
++++++++++++++++++++++++++

+-------------------+-------------+
| IR Ear Signal     | C.H.I.P Pin |
+===================+=============+
| left              | XIO-P2      |
+-------------------+-------------+
| right             | XIO-P4      |
+-------------------+-------------+

Note: These sensor circuits are not great. Their detection range is only of a couple of inches.
Our future reference design will include `a PCB with a Silicon Labs I2C MEMS
IR sensor <https://upverter.com/ductape/aef33f7c39fd29d5/rovercode-prox-sensor/>`_, which should work much better.

webcam -- the eye
-------------------
:important note: The default CHIP kernel does not enable the USB Video Class (UVC) driver. In the future we hope to provide a ready-to-use eMMC image with this driver included, but for now you'll have to rebuild the kernel with the UVC driver included. This is a more advanced task. Your best bet is `this tutorial <http://www.raspibo.org/wiki/index.php/Compile_the_Linux_kernel_for_Chip:_my_personal_HOWTO>`_. If you're not up for this, don't worry -- just stay tuned for an update to this page telling you where you can get a ready-to-use eMMC image.

At the moment, the webcam streaming service is not installed or
started with the main rovercode service (we have `an issue card
<https://github.com/aninternetof/rovercode/issues/110>`_ to fix this). So,
you'll need to get and run mjpg-streamer yourself for now.

Get and build mjpg-streamer by following steps 1 through 5 in `these
instructions <https://blog.miguelgrinberg.com/post/how-to-build-and-run-mjpg-streamer-on-the-raspberry-pi>`_.

To make mjpg-start on boot, add this line to `/etc/rc.local`. Replace {BUILD_DIR} with the absolute path to the directory where you built
mjpg-streamer.

.. code-block:: guess

    {BUILD_DIR}/mjpg_streamer -i "{BUILD_DIR}/input_uvc.so" -o "{BUILD_DIR}/output_http.so -w {BUILD_DIR}/www"

Restart the rover. You can check that mjpg-streamer has started by
pointing your PC's browser at `{ip-address-of-your-rover}:8080`. You should see
the mjpg-streamer demo page.

assembly
----------
Here is how it all hooks together:

.. image:: http://i.imgur.com/h9Y6mPG.png

Put everything on the chassis how you see fit. Below are some
photos of how we did it. Hot glue is your friend.

.. image:: http://i.imgur.com/p3TpMNj.jpg
.. image:: http://i.imgur.com/N0N6NQe.jpg
.. image:: http://i.imgur.com/TsyoME6.jpg

Note that the motors are still powered by the Thunder Tumbler AA
battery pack, so make sure there are batteries in there and
that the switch on the bottom is turned on when in use.

The webcam draws too much current to be directly connected to the
C.H.I.P's USB host port. So, we use a powered USB hub.

install rovercode service
--------------------------
Connect to the C.H.I.P. via serial or SSH.

Follow the Standard Setup on the `quickstart page <quickstart.html>`_.

play
------
Go to `<https://rovercode.com>`_, sign up for an account, then go to `Mission Control
<https://rovercode.com/mission-control>`_. Click `Connect to a Rover`. Choose
your rover, whose name is hardcoded `here <https://github.com/aninternetof/rovercode/blob/development/www/app.py#L148>`_,
sadly. You should see a message in the console bar on the right saying
that it has connected to a a rover and listing its local IP address.

Drag in some commands, hit play, and have fun!
