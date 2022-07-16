from safecracker.log import Log
from safecracker.motor.a4988 import A4988_Pins, A4988
from safecracker.motor.position import Position
from safecracker.motor.index import Index
from safecracker.motor.degrees import Degrees
from safecracker.motor.numbers import Numbers
import time


# acceleration_profile
def delay_profile(i, count):
    min_delay = 0.00001
    max_delay = 0.001
    ramp_steps = 1000
    if i < ramp_steps:
        delay = (min_delay - max_delay)/ramp_steps*i + max_delay
    elif ramp_steps <= i < (count - ramp_steps):
        delay = min_delay
    elif count-i <= ramp_steps:
        delay = (min_delay - max_delay)/ramp_steps*(count-i) + max_delay
    #print("{:f}".format(delay))
    return delay


class DefaultMotor(Log):
    #default_step_delay = 0.00075
    default_step_delay = 0.0005

    def __init__(self, a4988_pins, microsteps_per_step, full_step_degrees, index_pin, index_degrees, index_tolerance_degrees, numbers, numbers_tolerance, left_to_right, step_delay=None, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.driver = A4988(A4988_Pins(**a4988_pins), microsteps_per_step, parent=self)
        self.position = Position(self, int(360 / full_step_degrees * microsteps_per_step), parent=self)
        self.index = Index(self, index_pin, index_degrees, tolerance_degrees=index_tolerance_degrees, parent=self)
        self.degrees = Degrees(self, parent=self)
        self.numbers = Numbers(self, numbers, numbers_tolerance, left_to_right, parent=self)
        self.step_delay = step_delay or self.default_step_delay

    @Log.method(5)
    def step(self):
        self.driver.step()
        self.position.step()
        self.index.step()

    @Log.method(11)
    def steps(self, count):
        direction = bool(count > 0)
        count = abs(count)
        if self.driver.direction != direction:
            self.driver.direction = direction

        for i in range(count):
            self.step()
            if callable(self.step_delay):
                time.sleep(self.step_delay(i, count))
            else:
                time.sleep(self.step_delay)


