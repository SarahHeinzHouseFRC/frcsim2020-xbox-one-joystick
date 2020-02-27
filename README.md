# Controller #

This project is designed to connect an Xbox 360 or Xbox One controller to the FRC sim. Upon connecting a controller over
USB and launching this application, the user can send commands from the joystick to the sim core via UDP as JSON, which
will be conveyed to the sim. The core will send back a simple heartbeat signal to let the joystick know it's connected.

This project uses Python 3 and is built on top of the [xbox360controller](https://pypi.org/project/xbox360controller/)
pip library. This library was chosen over `xboxdrv` because:
  - It does not require sudo privileges
  - It contains access to more buttons, such as the buttons under the left and right joysticks
  - It allows feedback in the form of rumble and control of the LED status lights

## Installation ##
```sh
sudo apt install python3-pip
pip3 install -U xbox360controller
```
