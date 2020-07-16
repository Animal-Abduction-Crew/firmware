import pigpio
import time
from driver import Driver
from motor import Motor

pi = pigpio.pi()
left_motor = Motor(pi, [12,7,8])
right_motor = Motor(pi, [18,15,14])
driver = Driver(pi, left_motor, right_motor)

done = False

while not done:

    action = input('what do?')

    if action == 'w':
        driver.forward(1,100)
    elif action == 's':
        driver.reverse(1,100)
    elif action == 'a':
        driver.turn_left(0.2,100)
    elif action == 'd':
        driver.turn_right(0.2,100)
    elif action == 'exit':
        done = True

pi.stop()