#!/usr/bin/python2

import pigpio

g = None


def init():
    global g
    g = pigpio.pi()


def finish():
    g.stop()


class GpioGeneral:
    channel = None
    val = 0

    def __init__(self, channel):
        self.channel = channel

    def inc_val(self, val):
        return self.set_val(self.val + val)

    def dec_val(self, val):
        return self.set_val(self.val - val)

    def set_val(self, inp):
        if inp <= 0:
            inp = 0
        elif inp >= 1000:
            inp = 1000

        self.val = inp
        self.set_raw_val(inp)
        return self.val


class Servo(GpioGeneral):
    def __init__(self, channel):
        GpioGeneral.__init__(self, channel)
        g.set_mode(self.channel, pigpio.OUTPUT)

    def set_raw_val(self, pos):  # pos 0 to 1000
        assert 0 <= pos <= 1000
        g.set_servo_pulsewidth(self.channel, 1000 + pos)

    def start(self):
        self.set_val(0)

    def stop(self):
        g.set_servo_pulsewidth(self.channel, 0)


class DimmableLed(GpioGeneral):
    def __init__(self, channel):
        GpioGeneral.__init__(self, channel)
        g.set_mode(self.channel, pigpio.OUTPUT)
        g.set_PWM_range(self.channel, 1000)
        g.set_PWM_frequency(self.channel, 100)

    def set_raw_val(self, bri):  # bri 0 to 1000
        assert 0 <= bri <= 1000
        g.set_PWM_dutycycle(self.channel, bri)

    def start(self):
        self.set_val(1000)
