from safecracker.log import Log
from safecracker.motor.a4988 import A4988_Pins, A4988
from safecracker.motor.position import Position
from safecracker.motor.index import Index
from safecracker.motor.degrees import Degrees
from safecracker.motor.numbers import Numbers
import time


class DefaultMotor(Log):
    default_step_delay = 0.00001

    def __init__(self, a4988_pins, microsteps_per_step, full_step_degrees, index_pin, index_degrees, index_tolerance_degrees, numbers, numbers_tolerance, left_to_right, step_delay=None, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.driver = A4988(A4988_Pins(**a4988_pins), microsteps_per_step, parent=self)
        self.position = Position(self, int(360 / full_step_degrees * microsteps_per_step), parent=self)
        self.index = Index(self, index_pin, index_degrees, tolerance_degrees=index_tolerance_degrees, parent=self)
        self.degrees = Degrees(self, parent=self)
        self.numbers = Numbers(self, numbers, numbers_tolerance, left_to_right, parent=self)
        self.step_delay = step_delay or self.default_step_delay

    @Log.method(3)
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
                self.step_delay(i, count, self.step_delay)
            else:
                time.sleep(self.step_delay)
