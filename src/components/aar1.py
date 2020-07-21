import pigpio
import time

from components.light_sensor import LightSensor
from components.driver import Driver
from components.motor import Motor
from components.object_detector import ObjectDetector
from components.advanced_driver import AdvancedDriver

class AAR1:

    line_detected = False

    def __init__(self, pi, driver, adv_driver, detector):
        self.pi = pi
        self.driver = driver
        self.adv_driver = adv_driver
        self.detector = detector

        # Create line detector callback
        def line_detected_cb():
            if not self.line_detected:
                print('line detected!')
            self.line_detected = True

        self.left_line_detector = LightSensor(pi=pi, pin=2, callback=line_detected_cb)
        self.right_line_detector = LightSensor(pi=pi, pin=3, callback=line_detected_cb)

    def rescue(self, animal):

        self.line_detected = False

        done = False
        min_confidence = 0.6
        drive_straight_correction = 0

        start = time.time()

        while not done:
            try:
                detections = self.detector.detect()

                if detections is not None:

                    for detection in detections:

                        # adjust confidence based on animals in the field
                        if detection['name'] == 'tiger' and animal == 'cat':
                            min_confidence = 0.7
                        if detection['name'] == 'cat' and animal == 'tiger':
                            min_confidence = 0.7

                        if detection['name'] == animal and detection['confidence'] > min_confidence:
                            if self.adv_driver.adjust_to_target(detection):
                                # push it out
                                self.line_detected = False
                                while not self.line_detected:
                                    self.driver.forward(0.1,100)
                                self.driver.forward(0.2,100)
                                self.driver.reverse(1.5,90)
                                self.driver.turn_right(1,80)
                                self.driver.turn_left(1,80)
                                self.driver.stop()
                                done = True
                                # reset confidence
                                min_confidence = 0.6
                        else:
                            # search
                            if self.line_detected:
                                self.driver.reverse(1,70)
                                self.driver.turn_left(.3, 70)
                                self.line_detected = False

                            else:
                                if drive_straight_correction >= 3:
                                    drive_straight_correction = 0
                                    self.driver.turn_right(0.10, 10)

                                drive_straight_correction = drive_straight_correction + 1
                                self.driver.forward(0.75,100)
                else:
                    # search
                    if self.line_detected:
                        self.driver.reverse(1,70)
                        self.driver.turn_left(.3, 70)
                        self.line_detected = False

                    else:
                        if drive_straight_correction >= 3:
                            drive_straight_correction = 0
                            self.driver.turn_right(0.10, 10)

                        drive_straight_correction = drive_straight_correction + 1
                        self.driver.forward(0.75,100)

            except Exception as ex:
                print(ex)
                done = True
                print('THERE WAS AN ERROR DURING THE RESCUE MISSION')
                self.driver.stop()

        print(f"i ran for {time.time() - start}s")
        self.driver.stop()
