# ControlGeek Server
This is the server component of ControlGeek, a gesture-based home automation control system built at HackMIT 2016 (see Devpost page [here](http://devpost.com/software/controlgeek)).

ControlGeek Server is meant to be run on a Raspberry Pi hooked up various hardware such as LEDs and servos. The server communicates with the hardware through [pigpio](http://abyz.co.uk/rpi/pigpio/index.html) library and daemon. It then exposes a WebSockets interface allowing any WebSocket client to control the hardware.

At this point, ControlGeek Server is essentially a Proof of Concept. It is pre-alpha quality software and feature-incomplete.

ControlGeek Server is Free Software licensed under the AGPLv3+. See [COPYING](https://github.com/icasdri/ControlGeek-Server/blob/master/COPYING) for details.
