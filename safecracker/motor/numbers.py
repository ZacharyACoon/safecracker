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

    @Log.method(5)
    def number_to_position(self, number):
        number *= -1 if self.left_to_right else 1
        position = int(number * self.motor.position.positions / self.numbers) % self.motor.position.positions
        return position

    @Log.method(logging.INFO)
    def relative(self, number):
        number *= -1 if self.left_to_right else 1
        relative_steps = int(number * self.motor.position.positions / self.numbers)
        self.motor.steps(relative_steps)

    @Log.method(logging.INFO)
    def absolute(self, number, direction=None):
        target = self.number_to_position(number)
        relative_steps = self.motor.position.absolute_to_relative(target, direction)
        self.motor.steps(relative_steps)
