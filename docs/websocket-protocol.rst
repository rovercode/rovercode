websocket protocol
====================

Heartbeat
----------
.. code-block:: json

    {
       "type": "heartbeat"
    }

Motor Commands
-----------------

.. code-block:: json

    {
       "type": "motor-command",
       "motor-id": "motor-left",
       "motor-value": 84,
       "direction": "forward",
       "unit": "percent"
    }

LED Commands
-----------------

.. code-block:: json

    {
       "type": "chainable-rgb-led-command",
       "led-id": 0,
       "red-value": 84,
       "green-value": 255,
       "blue-value": 0,
    }


Sensor Readings
----------------

.. code-block:: json

    {
       "type": "sensor-reading",
       "sensor-type": "distance",
       "sensor-id": "ultrasonic-left",
       "sensor-value": 42,
       "unit": "cm"
    }

.. code-block:: json

    {
       "type": "sensor-reading",
       "sensor-type": "binary",
       "sensor-id": "bumper-front",
       "sensor-value": false,
       "unit": "active-high"
    }
