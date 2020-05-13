#Greifer        öffnen          5
#               schließen       6
#               geschwindigkeit 13 (PWM)
#Rad links      vorwärts       7
#               rückwärts      8
#               geschwindigkeit 12 (PWM)
#Rad rechts     vorwärts        15
#               rückwärts       14
#               geschwindigkeit 18 (PWM)
#

import pigpio
import time

# @pre pigpio demon must be running (sudo pigpiod)
# Hardware PWM available for GPIO 12, 13, 18, 19 (BCM scheme)

GPIO_PWM = 18 # PWM pin
GPIO_IN1 = 14 # motor control pin
GPIO_IN2 = 15 # motor control pin

RUNNING_TIME = 1 # seconds
PWM_FREQUENCY = 50000 # Hz
PWM_DUTY_CYCLE = 10 # percent

pi = pigpio.pi()

# Motor control pins
# 0, 1 forward (whatever that means in your case)
# 1, 0 reverse
# 1, 1 brake
# 0, 0 stop slowly

pi.set_mode(GPIO_IN1, pigpio.OUTPUT)
pi.set_mode(GPIO_IN2, pigpio.OUTPUT)
pi.write(GPIO_IN1, 0)
pi.write(GPIO_IN2, 1)

try:
    duty = PWM_DUTY_CYCLE * 10000 # Max: 1M
    pi.hardware_PWM (GPIO_PWM, PWM_FREQUENCY, duty)
    print('Hardware PWM on GPIO ' + str(GPIO_PWM) + ' enabled')
    print('Frequency: ' + str(pi.get_PWM_frequency(GPIO_PWM)) + ' Hz')
    print('Dutycycle: ' + \
          str(pi.get_PWM_dutycycle(GPIO_PWM) / 10000) + ' percent')
    print('Running for ' + str(RUNNING_TIME) + ' seconds')
    running = True
except:
    print('Hardware PWM not available on GPIO ' + str(GPIO_PWM))
    pi.stop()

if running:
    time.sleep(RUNNING_TIME)
    print('Shutting down')
    # Disable PWM
    pi.write(GPIO_PWM, 0)
    # Free resources
    pi.stop()