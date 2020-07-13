import pigpio
import time

# @pre pigpio demon must be running (sudo pigpiod)
# Hardware PWM available for GPIO 12, 13, 18, 19 (BCM scheme)

GPIO_PWM = 13 # PWM pin
GPIO_IN1 = 5 # motor control pin
GPIO_IN2 = 6 # motor control pin
PWM_FREQUENCY = 50000 # Hz

def grap(direction):

    pi = pigpio.pi()
    pi.set_mode(GPIO_IN1, pigpio.OUTPUT)
    pi.set_mode(GPIO_IN2, pigpio.OUTPUT)

    if(direction==1):
        pi.write(GPIO_IN1, 1)
        pi.write(GPIO_IN2, 0)
        RUNNING_TIME = 2
        PWM_DUTY_CYCLE = 60 # percent


    if(direction==0):
        pi.write(GPIO_IN1, 0)
        pi.write(GPIO_IN2, 1)
        RUNNING_TIME = 2
        PWM_DUTY_CYCLE = 60 # percent

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
        pi.write(GPIO_PWM, 1)
        # Free resources
        pi.stop()

grap(0)


