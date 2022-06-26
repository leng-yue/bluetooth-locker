import argparse
import os
import time
import subprocess as sp
from loguru import logger

parser = argparse.ArgumentParser()
parser.add_argument(
    "-d", "--device", action="append", help="<Required> Add Device", required=True
)
config = parser.parse_args()

addresses = [i.lower() for i in config.device]
previous_connected = True

while True:
    logger.debug("Looping...")
    connected = False

    for address in addresses:
        try:
            output = sp.check_output(
                ["bluetoothctl", "connect", address]
            ).decode("utf-8")
        except sp.CalledProcessError as e:
            output = e.output.decode("utf-8")

        if "Connection successful" in output or "already-connected" in output:
            connected = True
            logger.debug(f"{address} is connected")
            break
        else:
            logger.debug(f"{address} is not connected")

    logger.debug(f"Connected: {connected}")

    if connected != previous_connected:
        previous_connected = connected

        if connected is False:
            os.system("loginctl lock-session")
            logger.info("Locked session")
        else:
            os.system("loginctl unlock-session")
            logger.info("Unlocked session")

    time.sleep(5)
