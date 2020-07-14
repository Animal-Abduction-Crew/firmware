import pigpio
import asyncio

class Driver():
    
    def __init__(self, pi, left_motor, right_motor):
        self.pi = pi
        self.left = left_motor
        self.right = right_motor

    async def forward(self, duration, power):
        print('diving forward')

    def reverse(self, duration, power):
        print('diving forward')

    def turn_left(self, duration, power):
        print('turning left')

    def turn_right(self, duration, power):
        print('turning right')