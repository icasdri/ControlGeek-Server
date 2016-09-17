#!/usr/bin/python2

from time import sleep
import RPi.GPIO as g


g.setmode(g.BCM)


class Servo:
    channel = None
    pwm = None

    def __init__(self, channel):
        self.channel = channel
        g.setup(self.channel, g.OUT)

        freq, _ = Servo.freq_for_angle(0)
        self.pwm = g.PWM(self.channel, freq)

    @staticmethod
    def freq_for_angle(angle):
        u = 1500 + (angle / 45) * 500
        d = u / (u + 5)
        x = 1000000 / u
        return (x, d)

    def set_angle(self, angle):
        freq, duty = Servo.freq_for_angle(angle)
        self.pwm.ChangeFrequency(freq)
        # self.pwm.ChangeDutyCycle(duty)

    def start(self):
        _, duty = Servo.freq_for_angle(0)
        self.pwm.start(60)

    def stop(self):
        self.pwm.stop()


class LedLight:
    channel = None

    def __init__(self, channel):
        self.channel = channel
        g.setup(self.channel, g.OUT)

    def turn_on(self):
        g.output(self.channel, g.HIGH)

    def turn_off(self):
        g.output(self.channel, g.LOW)


led = LedLight(15)
se = Servo(14)

try:
    led.turn_on()
    se.start()
    sleep(5)

    while True:
        led.turn_off()
        se.set_angle(45)
        sleep(5)

        led.turn_on()
        se.set_angle(0)
        sleep(5)
except KeyboardInterrupt:
    pass  # proceed to exit code

led.turn_off()
g.cleanup()
