import pigpio
import time
from driver import Driver
from motor import Motor

pi = pigpio.pi()
left_motor = Motor(pi, [12,7,8])
right_motor = Motor(pi, [18,15,14])
driver = Driver(pi, left_motor, right_motor)

for i in range(1,20):
    driver.turn_left(0.02, 100)
    time.sleep(0.5)

pi.stop()