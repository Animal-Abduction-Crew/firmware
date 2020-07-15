import pigpio

class LightSensor:

    def __init__(self, pi, pin, callback):
        self.pi = pi
        self.callback = callback
        self.PIN = pin
        self.IGNORE_INTERVAL = 50000000
        self.HIGH = 0
        self.TALLY = 0
        self.LAST_TICK = pi.get_current_tick()

        pi.set_mode(self.PIN, pigpio.INPUT)

        def level_changed(gpio_num, level, tick):  
            self.TALLY += 1
            # Make sure gpio is HIGH (we want to detect rising edge).
            # Calls within IGNORE_INTERVAL are considered as single call.
            if ((self.pi.read(gpio_num) == self.HIGH) and (tick - self.LAST_TICK > self.IGNORE_INTERVAL)):
                self.LAST_TICK
                self.callback()
                print(self.TALLY)
                print(tick - self.LAST_TICK)
            
        pi.callback(self.PIN, pigpio.RISING_EDGE, level_changed)
