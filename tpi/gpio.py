#!/usr/bin/python2

import pigpio
from time import sleep

g = None


def init():
    global g
    g = pigpio.pi()


def finish():
    g.stop()


class Servo:
    channel = None

    def __init__(self, channel):
        self.channel = channel
        g.set_mode(self.channel, pigpio.OUTPUT)

    def set_pos(self, pos):  # pos 0 to 1000
        assert 0 <= pos <= 1000
        g.set_servo_pulsewidth(self.channel, 1000 + pos)

    def start(self):
        self.set_pos(0)

    def stop(self):
        g.set_servo_pulsewidth(self.channel, 0)


class DimmableLed:
    channel = None

    def __init__(self, channel):
        self.channel = channel
        g.set_mode(self.channel, pigpio.OUTPUT)
        g.set_PWM_range(self.channel, 1000)
        g.set_PWM_frequency(self.channel, 100)

    def set_bri(self, bri):  # bri 0 to 1000
        assert 0 <= bri <= 1000
        g.set_PWM_dutycycle(self.channel, bri)

    def start(self):
        self.set_bri(1000)


def main():
    init()
    se = Servo(14)
    led = DimmableLed(15)

    try:
        while True:
            for i in xrange(0, 1001):
                se.set_pos(i)
                led.set_bri(i)
                sleep(0.05)
            sleep(2)
            for i in xrange(1000, -1, -1):
                se.set_pos(i)
                led.set_bri(i)
                sleep(0.05)
            sleep(2)
    except KeyboardInterrupt:
        pass  # proceed to exit

    finish()
