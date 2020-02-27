#
# Copyright (c) 2019 FRC Team 3260
#

import signal
from xbox360controller import Xbox360Controller
from comms import *
from threading import Thread


class CommsThread(Thread):
    def __init__(self, comms_config, controller_state, verbose):
        super(CommsThread, self).__init__()
        self.verbose = verbose
        self.comms = Comms(comms_config)
        self.controller_state = controller_state

    def run(self):
        while True:
            # Send controller state
            tx_msg = self.controller_state.toJson()
            self.comms.tx(tx_msg)
            if self.verbose:
                print("Joystick transmit: " + tx_msg)

            # Receive heartbeat
            rx_msg = self.comms.rx()
            if rx_msg is None:
                print("Disconnected")
            else:
                if self.verbose:
                    print("Joystick received: " + rx_msg.decode("utf-8"))
                self.controller_state.collision = int(rx_msg[1:7])

    def join(self, **kwargs):
        Thread.join(self)


class PhysicalXboxController:
    def __init__(self, comms_config, verbose):
        self.controller_state = ControllerState()

        # Launch comms thread
        self.comms = CommsThread(comms_config, self.controller_state, verbose)
        self.comms.daemon = True
        self.comms.start()
        print("Controller: Launched")

        try:
            with Xbox360Controller(0, axis_threshold=0.0) as self.controller:
                # Button events
                self.controller.button_a.when_pressed = self.on_a_button_pressed
                self.controller.button_b.when_pressed = self.on_b_button_pressed
                self.controller.button_x.when_pressed = self.on_x_button_pressed
                self.controller.button_y.when_pressed = self.on_y_button_pressed
                self.controller.hat.when_moved = self.on_dpad_pressed

                # Left and right joysticks
                self.controller.axis_l.when_moved = self.on_left_joystick_moved
                self.controller.axis_r.when_moved = self.on_right_joystick_moved

                while True:
                    self.controller.set_rumble(self.controller_state.collision*0.2, self.controller_state.collision*0.2,
                                               duration=100)
                    time.sleep(0.1)

                signal.pause()
        except KeyboardInterrupt:
            pass

    def on_a_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))

    def on_b_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))

    def on_x_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))

    def on_y_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))

    def on_dpad_pressed(self, axis):
        self.controller_state.dpad.right.pressed = axis.x == 1
        self.controller_state.dpad.left.pressed = axis.x == -1
        self.controller_state.dpad.up.pressed = axis.y == 1
        self.controller_state.dpad.down.pressed = axis.y == -1
        print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))

    def on_left_joystick_moved(self, axis):
        self.controller_state.left_joystick.x = axis.x * 512
        self.controller_state.left_joystick.y = -axis.y * 512

    def on_right_joystick_moved(self, axis):
        self.controller_state.right_joystick.x = axis.x * 512
        self.controller_state.right_joystick.y = -axis.y * 512

    def rumble(self):
        self.controller.set_rumble(0.5, 0.5, 1000)
