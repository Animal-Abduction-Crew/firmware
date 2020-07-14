import pigpio

class Vehicle():
    
    def __init__(self, pi):
        self.pi = pi
        print('hello')

    def forward(self, duration, power):
        print('diving forward')

    def reverse(self, duration, power):
        print('diving forward')

    def turn_left(self, duration, power):
        print('turning left')

    def turn_right(self, duration, power):
        print('turning right')