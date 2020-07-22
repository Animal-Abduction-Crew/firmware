import pigpio
import time

from light_sensor import LightSensor
#from driver import Driver
#from motor import Motor

# Create gpio controller
print('init gpio controller')
pi = pigpio.pi()

# Create line detector
line_detected = False
def line_detected_cb():
    global line_detected
    line_detected = True
    print('line detected')

def something_infront_cb():
    print('something infront detected')

# init line detectors
print('init left line sensor')
left_line_detector = LightSensor(pi=pi, pin=2, callback=line_detected_cb)
right_line_detector = LightSensor(pi=pi, pin=3, callback=line_detected_cb)

# init front light sensor
print('init front proximity sensor')
front_proximity_sensor = LightSensor(pi=pi, pin=4, callback=something_infront_cb)

# init motors
# print('init motors')
# left_motor = Motor(pi, [12,7,8])
# right_motor = Motor(pi, [18,15,14])

# # init driver
# print('init driver')
# driver = Driver(pi, left_motor, right_motor)

while True:
    try:
        pass

    except KeyboardInterrupt:
        # driver.stop()
        print('User interrupt')
        break

# Free resources
print('Shutting down')
# driver.stop()
pi.stop()