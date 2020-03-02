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
    args = parser.parse_args()

    # Read config file
    with open(DEFAULT_CONFIG) as f:
        data = yaml.load(f)
        comms_config = {
            "rx_ip": "127.0.0.1",
            "rx_port": data['joystick']['port'],
            "tx_ip": data['core']['ip'],
            "tx_port": data['core']['joystickPort']
        }
    print("Receiving at %s:%d" % (comms_config["rx_ip"], comms_config["rx_port"]))
    print("Transmitting to %s:%d" % (comms_config["tx_ip"], comms_config["tx_port"]))

    xbox_controller = PhysicalXboxController(comms_config, args.verbose)


if __name__ == '__main__':
    main()
