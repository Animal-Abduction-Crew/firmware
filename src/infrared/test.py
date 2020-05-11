import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
pin = 2 
gpio.setup(pin, gpio.IN)

while  True:
    print(gpio.input(pin))
    time.sleep(1)
