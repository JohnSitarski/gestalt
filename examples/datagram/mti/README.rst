The example in this directory uses the MTI Datagram endpoint to build a
sender and a receiver application. The endpoint in each file is created
with its content type set to PROTOBUF and a Position protobuf object is
registered with a type identifier of 1. This allows a Position object to
be passed into the send function to be automatically PROTOBUF encoded
when sent and automatically PROTOBUF decoded upon receipt.

In one terminal start the receiver.

.. code-block:: console

    (venv) $ python receiver.py --log-level debug

In another terminal open the sender which will send a message to the remote
address every second.

.. code-block:: console

    (venv) $ python sender.py --log-level debug

Upon receipt of a message the receiver will print it to stdout.
