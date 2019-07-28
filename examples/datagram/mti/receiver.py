import asyncio
import logging
from gestalt.serialization import CONTENT_TYPE_PROTOBUF
from gestalt.datagram.mti import MtiDatagramEndpoint
from position_pb2 import Position


if __name__ == "__main__":

    import argparse
    from gestalt.runner import run

    ARGS = argparse.ArgumentParser(description="UDP Receiver Example")
    ARGS.add_argument(
        "--host",
        metavar="<host>",
        type=str,
        default="localhost",
        help="The host the receiver will running on",
    )
    ARGS.add_argument(
        "--port",
        metavar="<port>",
        type=int,
        default=53123,
        help="The port that the receiver will be listening on",
    )
    ARGS.add_argument(
        "--log-level",
        type=str,
        default="error",
        help="Logging level [debug|info|error]. Default is 'error'.",
    )

    args = ARGS.parse_args()

    try:
        numeric_level = getattr(logging, args.log_level.upper())
    except ValueError:
        raise Exception(f"Invalid log-level: {args.log_level}")

    logging.basicConfig(
        format="%(asctime)s.%(msecs)03.0f [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=numeric_level,
    )

    def on_message(data, **kwargs) -> None:
        addr = kwargs.get("addr")
        print(f"Received msg from {addr}: {data}")

    r = MtiDatagramEndpoint(on_message=on_message, content_type=CONTENT_TYPE_PROTOBUF)

    # Associate a message object with a unique message type identifier.
    type_identifier = 1
    r.register_message(type_identifier, Position)

    local_addr = (args.host, args.port)
    run(r.start(local_addr=local_addr), finalize=r.stop)