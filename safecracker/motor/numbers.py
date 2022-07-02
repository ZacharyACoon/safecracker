import logging
from safecracker.log import Log
import time


class Numbers(Log):
    def __init__(self, motor, numbers, tolerance, left_to_right=True, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.motor = motor
        self.numbers = numbers
        self.tolerance = tolerance
        self.left_to_right = left_to_right

    @Log.method(level=11, log_return=True)
    def number_to_position(self, number):
        number *= -1 if self.left_to_right else 1
        position = int(number * self.motor.position.positions / self.numbers)
        return position

    @Log.method
    def relative(self, number):
        relative_steps = self.number_to_position(number)
        self.motor.steps(relative_steps)

    @Log.method
    def absolute(self, number, direction=None):
        target = self.number_to_position(number)
        relative_steps = self.motor.position.absolute_to_relative(target, direction)
        self.motor.steps(relative_steps)
