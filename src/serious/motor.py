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

    # power in percent
    def forward(self, duration, power):

        self.pi.write(self.INPUT1_PIN, 1)
        self.pi.write(self.INPUT2_PIN, 0)

        try:
            duty = 10000 * power
            self.pi.hardware_PWM(self.PWM_PIN, self.PWM_FREQUENCY, duty)

        except:
            print('Hardware PWM not available on GPIO ')
            self.pi.stop()
            sys.exit(1)

        time.sleep(duration)

        self.pi.write(self.INPUT1_PIN, 1)
        self.pi.write(self.INPUT2_PIN, 1)

        self.pi.write(self.INPUT1_PIN, 0)
        self.pi.write(self.INPUT2_PIN, 0)

    def reverse(self, duration, power):
        # forward
        # stop
        pass

    
