import pigpio
import time

# My light sensor IDUINO ST1140 returns HIGH (3,3 V) for black
# and LOW (0 V) for white (contrary to data sheet).
# Sensor may be too sensitive when crossing white/black boundary
# (see below).
#
# This program is supposed to detect transitions from white to black.
#
# precondition: pigpiod demon must be running

GPIO_LIGHT = 4 # Lightsensor GPI2 pin
IGNORE_INTERVAL = 5000 # microseconds
HIGH = 1

tally = 0 # counter for callback function calls
last_tick = 0 # time of last valid callback function call

def level_changed(gpio_num, level, tick):
    global tally
    global pi
    global last_tick
    global IGNORE_INTERVAL
    global HIGH
    
    tally += 1
    # Make sure gpio is HIGH (we want to detect rising edge).
    # Calls within IGNORE_INTERVAL are considered as single call.
    if ((pi.read(gpio_num) == HIGH) and (tick - last_tick > IGNORE_INTERVAL)):
        print(f"{level} {tally} {((tick-last_tick)/1000000.):0.2f}")
        last_tick = tick


pi = pigpio.pi()
pi.set_mode(GPIO_LIGHT, pigpio.INPUT)
# Only LOW to HIGH is considered (rising edge). See logic in callback.
# Callback must be adapted for considering falling edge.
cb = pi.callback(GPIO_LIGHT, pigpio.RISING_EDGE, level_changed)

while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        print('User interrupt')
        break

# Free resources
print('Shutting down')
pi.stop()
