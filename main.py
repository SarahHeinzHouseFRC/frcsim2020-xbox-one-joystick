#!/usr/bin/python3

#
# Copyright (c) 2019 FRC Team 3260
#

import sys
import argparse
import yaml
from physicalcontroller import PhysicalXboxController

DEFAULT_CONFIG = "joystickConfig.yml"


def main():
    # Read command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("--usb", help="usb port number (0, 1, etc.)", type=int, default=0)
    parser.add_argument("--player", help="player 1-6", type=int, default=1)
    args = parser.parse_args()

    # Read config file
    # Add 10 to ports for each subsequent connected controller
    with open(DEFAULT_CONFIG) as f:
        data = yaml.safe_load(f)
        comms_config = {
            "rx_ip": "127.0.0.1",
            "rx_port": data['joystick']['port'] + 10 * (args.player - 1),
            "tx_ip": data['core']['ip'],
            "tx_port": data['core']['joystickPort'] + 10 * (args.player - 1)
        }

    print("Receiving at %s:%d" % (comms_config["rx_ip"], comms_config["rx_port"]))
    print("Transmitting to %s:%d" % (comms_config["tx_ip"], comms_config["tx_port"]))

    xbox_controller = PhysicalXboxController(args.player, args.usb, comms_config, args.verbose)


if __name__ == '__main__':
    main()
