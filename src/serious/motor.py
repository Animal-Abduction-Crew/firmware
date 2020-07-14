import sys
import time
import pigpio

class Motor:
    
    PWM_FREQUENCY = 50000

    def __init__(self, pi, pins):
        self.pi = pi
        self.PWM_PIN = pins[0]
        self.INPUT1_PIN = pins[1]
        self.INPUT2_PIN = pins[2]

        self.pi.set_mode(self.INPUT1_PIN, pigpio.OUTPUT)
        self.pi.set_mode(self.INPUT2_PIN, pigpio.OUTPUT)

    def forward(self, power):
        self._write(1,0)
        self._go(power)

    def reverse(self, power):
        self._write(0,1)
        self._go(power)

    def _go(self, power):
        try:
            duty = 10000 * power
            self.pi.hardware_PWM(self.PWM_PIN, self.PWM_FREQUENCY, duty)

        except:
            print('Hardware PWM not available on GPIO ')
            self.pi.stop()
            sys.exit(1)

    def stop(self):
        self._write(1,1)
        self._write(0,0)

    def _write(self, pin1, pin2):
        self.pi.write(self.INPUT1_PIN, pin1)
        self.pi.write(self.INPUT2_PIN, pin2)
