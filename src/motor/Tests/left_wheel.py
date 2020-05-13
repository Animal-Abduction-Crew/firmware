import pigpio
import time

# @pre pigpio demon must be running (sudo pigpiod)
# Hardware PWM available for GPIO 12, 13, 18, 19 (BCM scheme)

GPIO_PWM = 12 # PWM pin
GPIO_IN1 = 7 # motor control pin
GPIO_IN2 = 1 # motor control pin

#GPIO_PWM = 13 # PWM pin
#GPIO_IN1 = 27 # motor control pin
#GPIO_IN2 = 22 # motor control pin

RUNNING_TIME = 10 # seconds
PWM_FREQUENCY = 50000 # Hz
PWM_DUTY_CYCLE = 50 # percent

pi = pigpio.pi()

# For PWM on non-hardware-GPIO pins (here: 21)
#pi.set_mode(21, pigpio.OUTPUT)
#pi.set_PWM_frequency(21, PWM_FREQUENCY)
#pi.set_PWM_range(21, 100)
#pi.set_PWM_dutycycle(PWM_DUTY_CYCLE)

# Motor control pins
# 0, 1 forward (whatever that means in your case)
# 1, 0 reverse
# 1, 1 brake
# 0, 0 stop slowly
pi.set_mode(GPIO_IN1, pigpio.OUTPUT)
pi.set_mode(GPIO_IN2, pigpio.OUTPUT)
pi.write(GPIO_IN1, 0)
pi.write(GPIO_IN2, 0)

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
