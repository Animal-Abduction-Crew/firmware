import pigpio
import time

# @pre pigpio demon must be running (sudo pigpiod)
PWM_FREQUENCY = 50000


def initialize_pins(pi):
    for i in [14, 8, 15, 7]:
        pi.set_mode(i, pigpio.OUTPUT)


def drive(running_time, pi, power):
    PWM_DUTY_CYCLE = int(round(50 * power, 0))

    try:
        duty = PWM_DUTY_CYCLE * 10000  # Max: 1M
        for i in [18, 12]:
            pi.hardware_PWM(i, PWM_FREQUENCY, duty)
        running = True
    except:
        print('Hardware PWM not available on GPIO ')
        pi.stop()

    if running:
        time.sleep(running_time)
        for i in [18, 12]:
            pi.write(i, 0)
        pi.stop()


def brake():
    pi = pigpio.pi()
    initialize_pins(pi)

    for i in [14, 15, 7, 8]:
        pi.write(i, 1)

    drive(running_time=0.2, pi=pi, power=1)


def drive_straight(running_time, direction, power):
    pi = pigpio.pi()
    initialize_pins(pi)

    if direction == "forward":
        hi_low = [0, 1]
    elif direction == "backward":
        hi_low = [1, 0]

    for i in [14, 8]:
        pi.write(i, hi_low[0])

    for i in [15, 7]:
        pi.write(i, hi_low[-1])

    drive(running_time, pi, power)
    brake()


def drive_curve(running_time, direction, power):
    pi = pigpio.pi()
    initialize_pins(pi)

    if direction == "left":
        hi_low = [0, 1]
    elif direction == "right":
        hi_low = [1, 0]

    for i in [14, 7]:
        pi.write(i, hi_low[0])

    for i in [15, 8]:
        pi.write(i, hi_low[-1])

    drive(running_time, pi, power)
    brake()


drive_straight(running_time=0.2, direction="forward", power=1)
time.sleep(1)
drive_straight(running_time=0.2, direction="backward", power=1)
time.sleep(1)
drive_curve(running_time=0.2, direction="left", power=1)
time.sleep(1)
drive_curve(running_time=0.2, direction="right", power=1)
