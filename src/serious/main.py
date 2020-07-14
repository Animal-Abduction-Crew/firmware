import pigpio
import time

from line_detector import LineDetector
from driver import Driver
from motor import Motor

# Create gpio controller
print('init gpio controller')
pi = pigpio.pi()

# Create line detector
line_detected = False
def line_detected():
    global line_detected
    line_detected = True

# init line detectors
print('init left line sensor')
left_line_detector = LineDetector(pi=pi, pin=2, callback=line_detected)
right_line_detector = LineDetector(pi=pi, pin=3, callback=line_detected)

# init motors
print('init motors')
left_motor = Motor(pi, [12,7,8])
right_motor = Motor(pi, [18,15,14])

# init driver
print('init driver')
driver = Driver(pi, left_motor, right_motor)

while True:
    try:
        driver.turn_left(1,30)
        time.sleep(1)
        driver.turn_right(1,30)
        time.sleep(1)

    except KeyboardInterrupt:
        driver.stop()
        print('User interrupt')
        break

# Free resources
print('Shutting down')
driver.stop()
pi.stop()