websocket protocol
====================

Heartbeat
----------
.. code-block:: json

    {
       "type": "heartbeat",
    }

Motors Commands
-----------------

.. code-block:: json

    {
       "type": "motor-command",
       "motor-id": "motor-left",
       "motor-value": 84
    }

Sensor Readings
----------------

.. code-block:: json

    {
       "type": "sensor-reading",
       "sensor-type": "distance",
       "sensor-id": "ultrasonic-left",
       "sensor-value": 42
    }

.. code-block:: json

    {
       "type": "sensor-reading",
       "sensor-type": "binary",
       "sensor-id": "bumper-front",
       "sensor-value": false
    }
