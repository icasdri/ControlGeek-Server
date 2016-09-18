#!/usr/bin/python2

from time import sleep
import RPi.GPIO as g


g.setmode(g.BCM)


class Servo:
    channel = None
    pwm = None
    freq = 50

    def __init__(self, channel):
        self.channel = channel
        g.setup(self.channel, g.OUT)

        self.pwm = g.PWM(self.channel, self.freq)

    def set_position(self, pos):  # pos out of 100
        # pw = (1000 + 1000 * pos / 100) / 1000000
        # duty = pw * self.freq * 100
        self.pwm.ChangeDutyCycle(5 + 5 * pos / 100)

    def start(self):
        self.pwm.start(5)

    def stop(self):
        self.pwm.stop()


class OnOffLed:
    channel = None

    def __init__(self, channel):
        self.channel = channel
        g.setup(self.channel, g.OUT)

    def turn_on(self):
        g.output(self.channel, g.HIGH)

    def turn_off(self):
        g.output(self.channel, g.LOW)


class DimmableLed:
    channel = None
    pwm = None
    freq = 100

    def __init__(self, channel):
        self.channel = channel
        g.setup(self.channel, g.OUT)

        self.pwm = g.PWM(self.channel, self.freq)

    def set_brightness(self, bri):  # bri out of 100
        self.pwm.ChangeDutyCycle(bri)

    def start(self):
        self.pwm.start(100)


led = DimmableLed(15)
se = Servo(14)

try:
    led.start()
    se.start()

    while True:
        for i in xrange(0, 101):
            led.set_brightness(i)
            se.set_position(i)
            sleep(0.1)
        sleep(1)
        for i in xrange(100, -1, -1):
            led.set_brightness(i)
            se.set_position(i)
            sleep(0.1)

except KeyboardInterrupt:
    pass  # proceed to exit code

led.turn_off()
g.cleanup()
