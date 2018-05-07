# alesisvsysex

Python tool for configuring Alesis VMini MIDI controllers

I modified the tool to work with the Alesis VMini from the original code that was to do with the V-25.


from https://github.com/le1ca/alesisvsysex



## Overview

The official tool for configuring these controllers only works on Windows. Fortunately, I was able to [reverse engineer the SysEx protocol](https://lo.calho.st/projects/reverse-engineering-the-alesis-v-series-sysex-protocol/) and implement this (eventually) cross-platform tool.

Currently, this software is only known to work on Linux, and probably only supports the Alesis V-25 controller. It includes a model for the parts of the SysEx protocol I was able to reverse (i.e., most of it), the ability to fetch and update the device config, and the ability to store and load configurations as files.

The GUI uses [PyQt5](http://pyqt.sourceforge.net/Docs/PyQt5/), and the MIDI layer uses [mido](https://mido.readthedocs.io/en/latest/).

## Dependencies

This software is written for Python 3.5+. It requires a system installation of PyQt5. Installing this dependency looks something like this on Ubuntu:

`sudo apt-get install python3-pyqt5`

The remaining dependencies can be installed in a virtualenv using pip:

`pip3 install -r requirements.pip3`

## Launching the application

From this directory, you can run `python3 -malesisvsysex` to launch the GUI.

An exception will immediately be thrown if the MIDI controller cannot be detected. If you unplug the controller after starting the application, you're in for a bad time. Eventually I'll make this more well-behaved, but for time time being just make sure the device is plugged in before you start.

## Running the test suite

From the same directory that you can launch the application, you can run `python3 -munittest` to run the test suite.

## Contributing

Any contributions of bug fixes or improvements will be greatly appreciated, including adding support for a different OS or controller.

## License

This software is released under the terms of the MIT license. A copy of the license can be found in the `LICENSE` file.

