import time

import pigpio

class Driver():
    
    def __init__(self, pi, left_motor, right_motor):
        self.pi = pi
        self.left = left_motor
        self.right = right_motor

    def forward(self, duration, power):
        self.left.forward(power)
        self.right.forward(power)
        time.sleep(duration)
        self.stop()

    def reverse(self, duration, power):
        self.left.reverse(power)
        self.right.reverse(power)
        time.sleep(duration)
        self.stop()

    def turn_left(self, duration, power):
        self.left.reverse(power)
        self.right.forward(power)
        time.sleep(duration)
        self.stop()

    def turn_right(self, duration, power):
        self.left.forward(power)
        self.right.reverse(power)
        time.sleep(duration)
        self.stop()

    def stop(self):
        self.left.stop()
        self.right.stop()