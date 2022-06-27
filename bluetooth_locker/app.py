import argparse
import logging
import os
import subprocess as sp
import time
from pathlib import Path

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


def check_privileges():
    if not os.environ.get("SUDO_UID") and os.geteuid() != 0:
        raise PermissionError("You need to run this script with sudo or as root.")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--device", action="append", help="<Required> Add Device", required=True
    )
    parser.add_argument(
        "--install", action="store_true", help="Install bluetooth-locker"
    )
    parser.add_argument(
        "--uninstall", action="store_true", help="Uninstall bluetooth-locker"
    )
    parser.add_argument(
        "--service-path",
        help="Path to bluetooth-locker service file",
        default="/etc/systemd/system/bluetooth-locker.service",
    )

    return parser.parse_args()


def lock_unlock_sessions(lock=True):
    sessions_text = sp.check_output(["loginctl", "list-sessions"]).decode("utf-8")
    lines = sessions_text.split("\n")

    for line in lines:
        if "SESSION" in line:
            continue
        if "sessions listed" in line:
            continue
        splits = line.strip().split(" ")
        if len(splits) < 2:
            continue
        session_id = int(splits[0])

        if lock:
            os.system(f"loginctl lock-session {session_id}")
            logging.info(f"Locked session {session_id}")
        else:
            os.system(f"loginctl unlock-session {session_id}")
            logging.info(f"Unlocked session {session_id}")


def loop(config):
    addresses = [i.lower() for i in config.device]
    previous_connected = True

    while True:
        logging.debug("Looping...")
        connected = False

        for address in addresses:
            try:
                output = sp.check_output(["bluetoothctl", "connect", address]).decode(
                    "utf-8"
                )
            except sp.CalledProcessError as e:
                output = e.output.decode("utf-8")

            if "Connection successful" in output or "already-connected" in output:
                connected = True
                logging.debug(f"{address} is connected")
                break
            else:
                logging.debug(f"{address} is not connected")

        logging.debug(f"Connected: {connected}")

        if connected != previous_connected:
            previous_connected = connected

            logging.info(f"Connection status changed to {connected}")
            lock_unlock_sessions(not connected)

        time.sleep(5)


def install(config):
    check_privileges()
    logging.info("Installing bluetooth-locker")

    service_path = Path(config.service_path)

    if service_path.exists():
        logging.warning(f"{service_path} already exists, overwriting...")

    devices = " ".join([f"-d {i.lower()}" for i in config.device])
    logging.info(f"Creating service file at {service_path}")

    template = "[Unit]\n"
    template += "Description=Bluetooth Locker\n"
    template += "After=network.target\n"
    template += "\n"
    template += "[Service]\n"
    template += "Type=simple\n"
    template += f"ExecStart=/usr/bin/python3 {__file__} {devices}\n"
    template += "Restart=always\n"
    template += "RestartSec=10s\n"
    template += "\n"
    template += "[Install]\n"
    template += "WantedBy=multi-user.target\n"

    logging.info(f"Generated service file:\n{template}")
    service_path.write_text(template)

    logging.info(f"Enabling service file at {service_path}")
    os.system(f"systemctl daemon-reload")
    os.system(f"systemctl enable bluetooth-locker")
    os.system(f"systemctl start bluetooth-locker")

    logging.info("Installation complete")


def uninstall(config):
    check_privileges()
    logging.info("Uninstalling bluetooth-locker")

    service_path = Path(config.service_path)
    if not service_path.exists():
        logging.error(f"{service_path} does not exist, skipping...")
        return

    logging.info(f"Disabling service file at {service_path}")
    os.system(f"systemctl disable bluetooth-locker")
    os.system(f"systemctl stop bluetooth-locker")
    service_path.unlink()
    os.system(f"systemctl daemon-reload")

    logging.info("Uninstallation complete")


def main():
    config = parse_args()

    if config.install:
        install(config)
    elif config.uninstall:
        uninstall(config)
    else:
        loop(config)


if __name__ == "__main__":
    main()
