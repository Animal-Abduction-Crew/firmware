from flask import Flask, render_template, jsonify
import pigpio

from components.light_sensor import LightSensor
from components.driver import Driver
from components.motor import Motor
from components.object_detector import ObjectDetector
from components.advanced_driver import AdvancedDriver
from components.simple_driver import SimpleDriver
from components.aar1 import AAR1

# init object detector
detector_settings = {
    "weights": "src/nets/256x192-yolo-tiny-3l_final.weights",
    "cfg": "src/nets/256x192-yolo-tiny-3l.cfg",
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

# init simple driver
print('init simple driver')
simple_driver = SimpleDriver(pi, left_motor, right_motor)

# init driver
print('init driver')
driver = Driver(pi, left_motor, right_motor)

# init advanced driver
print('init advanced_driver')
adv_driver = AdvancedDriver(driver, detector_settings['width'])

# init object detector
print('init object detector')
detector = ObjectDetector(detector_settings)

# init AAR1
print('init AAR1')
aar1 = AAR1(pi=pi, driver=driver, adv_driver=adv_driver, detector=detector)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rescue/<animal>')
def resuce(animal):

    if animal in ['elephant', 'tiger', 'star', 'cat', 'frog']:

        print(f"Ok, i'm going to resuce a(n) {animal}")

        aar1.rescue(animal)

        return 'OK'
    else:
        return f"WTF is a {animal}? I'm not going to do anything!"

@app.route('/control/<action>')
def control(action):

    power = 50

    if action == 'forward':
        print('remote control: go forward')
        simple_driver.forward(power)
        return 'Ok'

    elif action == 'reverse':
        print('remote control: go reverse')
        simple_driver.reverse(power)
        return 'Ok'

    elif action == 'left':
        print('remote control: turn left')
        simple_driver.turn_left(power)
        return 'Ok'

    elif action == 'right':
        print('remote control: turn right')
        simple_driver.turn_right(power)
        return 'Ok'

    elif action == 'stop':
        print('remote control: stop')
        simple_driver.stop()
        return 'Ok'
    
    return 'Error'

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=False)
