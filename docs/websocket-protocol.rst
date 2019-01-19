websocket protocol
====================

Heartbeat
----------
.. code-block:: json

    {
       "type": "heartbeat",
    }

Motor Commands
-----------------

.. code-block:: json

    {
       "type": "motor-command",
       "motor-id": "motor-left",
       "motor-value": 84,
       "unit": "percent"
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
