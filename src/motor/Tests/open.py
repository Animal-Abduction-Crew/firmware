import pigpio
import time

GPIO_PWM = 13 # PWM pin

RUNNING_TIME = 1 # seconds
PWM_FREQUENCY = 50000 # Hz
PWM_DUTY_CYCLE = 60 # percent

pi = pigpio.pi()

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
