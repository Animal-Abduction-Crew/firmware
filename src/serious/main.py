import pigpio
import time

from light_sensor import LightSensor
from driver import Driver
from motor import Motor
from object_detector import ObjectDetector
from advanced_driver import AdvancedDriver

# init object detector
detector_settings = {
    "weights": "nets/256x192-yolo-tiny-3l_final.weights",
    "cfg": "nets/256x192-yolo-tiny-3l.cfg",
    "width": 256,
    "height": 192,
    "min_confidence": 0.5,
    "threshold": 0.4
}

# Create gpio controller
print('init gpio controller')
pi = pigpio.pi()

# init motors
print('init motors')
left_motor = Motor(pi, [12,7,8])
right_motor = Motor(pi, [18,15,14])

# init driver
print('init driver')
driver = Driver(pi, left_motor, right_motor)

# init advanced driver
print('init advanced_driver')
adv_driver = AdvancedDriver(driver, detector_settings['width'])

detector = ObjectDetector(detector_settings)

# Create line detector
line_detected = False
def line_detected_cb():
    global line_detected
    if not line_detected:
        print('line detected!')
    line_detected = True

last_time_something_infront = None

def something_infront_cb():
    global last_time_something_infront
    last_time_something_infront = time.time()
    print('something infront detected')

# init line detectors
print('init left line sensor')
left_line_detector = LightSensor(pi=pi, pin=2, callback=line_detected_cb)
right_line_detector = LightSensor(pi=pi, pin=3, callback=line_detected_cb)

# init front light sensor
print('init front proximity sensor')
front_proximity_sensor = LightSensor(pi=pi, pin=4, callback=something_infront_cb)

min_confidence = 0.7

print('----------------------------------')
print('startup successfull')
print('----------------------------------')

done = False
drive_straight_correction = 0

def search():
    global drive_straight_correction
    global line_detected

    if line_detected:
        driver.reverse(1,70)
        driver.turn_left(.3, 70)
        line_detected = False
    
    else:
        if drive_straight_correction >= 3:
            drive_straight_correction = 0
            driver.turn_right(0.10, 10)
        
        drive_straight_correction = drive_straight_correction + 1
        driver.forward(0.75,100)

def push_it_out():
    global line_detected
    global done

    line_detected = False
    while not line_detected:
        driver.forward(0.1,100)
    driver.forward(0.2,100)
    driver.reverse(1.5,90)
    driver.turn_right(2,80)
    driver.stop()
    done = True

start = time.time()

while not done:
    try:
        detections = detector.detect()
        
        if detections is not None:
        
            for detection in detections:
                if detection['name'] == 'tiger' and detection['confidence'] > min_confidence:
                    if adv_driver.adjust_to_target(detection):
                        push_it_out()
                else:
                    search()
        else:
            search()

    except KeyboardInterrupt:
        print('user interrupt')
        break

print(f"i ran for {time.time() - start}s")

# Free resources
print('shutting down')
driver.stop()
pi.stop()

print('----------------------------------')
print('shutdown successfull')
print('----------------------------------')