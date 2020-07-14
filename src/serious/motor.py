import sys
import time
import pigpio
import asyncio

class Motor:
    
    PWM_FREQUENCY = 50000

    def __init__(self, pi, pins):
        self.pi = pi
        self.PWM_PIN = pins[0]
        self.INPUT1_PIN = pins[1]
        self.INPUT2_PIN = pins[2]

        self.pi.set_mode(self.INPUT1_PIN, pigpio.OUTPUT)
        self.pi.set_mode(self.INPUT2_PIN, pigpio.OUTPUT)

    async def forward(self, duration, power):
        self.write(1,0)
        await self.go(duration, power) 

    async def reverse(self, duration, power):
        self.write(0,1)
        await self.go(duration, power) 

    async def go(self, duration, power):
        try:
            duty = 10000 * power
            self.pi.hardware_PWM(self.PWM_PIN, self.PWM_FREQUENCY, duty)

        except:
            print('Hardware PWM not available on GPIO ')
            self.pi.stop()
            sys.exit(1)

        await asyncio.sleep(duration)

        self.write(1,1)
        self.write(0,0)

    def write(self, pin1, pin2):
        self.pi.write(self.INPUT1_PIN, pin1)
        self.pi.write(self.INPUT2_PIN, pin2)

    
