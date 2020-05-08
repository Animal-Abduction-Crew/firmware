import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
pin = 3 
gpio.setup(pin, gpio.IN)

while  True:
    print(gpio.input(pin))
    time.sleep(1)
