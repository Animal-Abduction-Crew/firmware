import pigpio
import time

class Fahren:

    # @pre pigpio demon must be running (sudo pigpiod)
    # Hardware PWM available for GPIO 12, 13, 18, 19 (BCM scheme)
    PWM_FREQUENCY = 50000

    def initialize_pins(self, pi):
        for i in [14, 8, 15, 7]:
            pi.set_mode(i, pigpio.OUTPUT)

    def drive(self, running_time, pi, power):
        PWM_DUTY_CYCLE = int(round(50 * power, 0))

        running = False

        try:
            duty = PWM_DUTY_CYCLE * 10000 # Max: 1M
            for i in [18, 12]:
                pi.hardware_PWM(i, PWM_FREQUENCY, duty)
            running = True
        except:
            print('Hardware PWM not available on GPIO ')
            pi.stop()

        if running:
            time.sleep(running_time)
            for i in [18, 12]:
                pi.write(i, 0)
            pi.stop()

    def brake(self):
        pi = pigpio.pi()
        self.initialize_pins(pi)

        for i in [14, 15, 7, 8]:
            pi.write(i, 1)
        
        self.drive(0.5, pi, 1)



    def drive_straight(self, running_time, direction, power):
        pi = pigpio.pi()
            for i in [14, 8, 15, 7]:
            pi.set_mode(i, pigpio.OUTPUT

        if direction == "forward":
            hi_low = [0, 1]
        elif direction == "reverse":
            hi_low = [1, 0]

        for i in [14, 8]:
            pi.write(i, hi_low[0])

        for i in [15, 7]:
            pi.write(i, hi_low[-1])

        self.drive(running_time, pi, power)
        self.brake()
