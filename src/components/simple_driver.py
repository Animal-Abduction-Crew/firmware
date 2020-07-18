import time

import pigpio

class SimpleDriver():
    
    def __init__(self, pi, left_motor, right_motor):
        self.pi = pi
        self.left = left_motor
        self.right = right_motor

    def forward(self, power):
        self.left.forward(power)
        self.right.forward(power)
    def reverse(self, power):
        self.left.reverse(power)
        self.right.reverse(power)

    def turn_left(self, power):
        self.left.reverse(power)
        self.right.forward(power)

    def turn_right(self, power):
        self.left.forward(power)
        self.right.reverse(power)

    def stop(self):
        self.left.stop()
        self.right.stop()
