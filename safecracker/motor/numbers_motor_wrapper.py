import logging
from safecracker.log import Log
import time


class NumbersMotorWrapper(Log):
    def __init__(self, degrees_motor_wrapper, numbers, tolerance, left_to_right=True, parent_logger=None):
        super().__init__(parent_logger)
        self.degrees_motor_wrapper = degrees_motor_wrapper
        self.numbers = numbers
        self.tolerance = tolerance
        self.left_to_right = left_to_right

    @Log.method(level=4)
    def _number_to_degrees(self, number):
        number *= -1 if self.left_to_right else 1
        degrees = 360 * number / self.numbers
        return degrees

    @Log.method
    def absolute(self, number, direction=None):
        degrees = self._number_to_degrees(number)
        self.degrees_motor_wrapper.absolute(degrees, direction=direction)

    @Log.method
    def relative(self, number):
        degrees = self._number_to_degrees(number)
        self.degrees_motor_wrapper.relative(degrees)
