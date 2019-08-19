websocket protocol
====================

Here is an example of a Rover config that the service might expect to
get from the server.

.. code-block:: json

    {
        "left-ultrasonic-port": 1,
        "right-ultrasonic-port": 2,
        "left-ultrasonic-threshold": 10,
        "right-ultrasonic-threshold": 10,
        "chainable-rgb-led-port": 7,
        "num-chainable-rgb-leds": 2
    }
