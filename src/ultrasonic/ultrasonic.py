import pigpio
import time

# @pre pigpio demon must be running (sudo pigpiod)

GPIO_ECHO = 21 # ultrasonic sensor input pin (echo)
GPIO_TRIG = 20 # ultrasonic sensor output pin (trigger)

SPEED_OF_SOUND = 343.2 # m per s
SEND_OFFSET = 250 # sensor warmup phase before sending (micro sec)

start_tick = 0 # trigger start time

def level_changed(gpio_num, level, tick):
    global pi
    global start_tick
    
    #print("Falling edge detected on GPIO {0}".format(gpio_num))
    
    run_time = (tick - start_tick - SEND_OFFSET) # micro sec
    dist = (run_time / 2) / 1e6 * SPEED_OF_SOUND
    print("Distance: {0:0.2f} m".format(dist))
    print("-----")     
        
pi = pigpio.pi()

pi.set_mode(GPIO_ECHO, pigpio.INPUT)
pi.set_mode(GPIO_TRIG, pigpio.OUTPUT)

# Called on HIGH to LOW (falling edge) on sensor output.
cb = pi.callback(GPIO_ECHO, pigpio.FALLING_EDGE, level_changed)

input("Start trigger (enter)")
while True:
    try:
        pi.set_pull_up_down(GPIO_ECHO, pigpio.PUD_DOWN)
        # Falling edge on sensor input triggers sending.
        pi.gpio_trigger(GPIO_TRIG, 10, 1)
        start_tick = pi.get_current_tick()
        time.sleep(0.1)
        input("Start trigger (enter)")
    except KeyboardInterrupt:
        print("User interrupt")
        break;
        
 # Free resources
print('Shutting down')
pi.stop()
