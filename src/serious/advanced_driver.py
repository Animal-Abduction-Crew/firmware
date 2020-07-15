class AdvancedDriver:

    POWER = 30
    MAGIC = 5
    TOLERANCE_PX = 4

    def __init__(self, driver, width):
        self.driver = driver
        self.WIDTH = width

    def adjust_to_target(self, detection):

        x = detection['x'] + ( detection['width'] / 2)
        half = self.WIDTH / 2

        if x < half + self.TOLERANCE_PX and x > half - self.TOLERANCE_PX:
            print('already centered. nothing to do!')
            return True
        
        if x < half:
            adjust_value = (1 - (x / half)) / self.MAGIC
            print(f"adjusting to the left for {adjust_value}s")
            self.driver.turn_left(adjust_value, self.POWER)

        elif x > half:
            adjust_value = (x - half) / (self.WIDTH - half) / self.MAGIC
            print(f"adjusting to the right for {adjust_value}s")
            self.driver.turn_right(adjust_value, self.POWER)

        return False