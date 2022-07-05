from safecracker.log import Log
import time
import logging


class Degrees(Log):
    def __init__(self, motor, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.motor = motor

    @property
    def degrees(self):
        return 360 * self.motor.position.position / self.motor.position.positions

    def degrees_to_position(self, degrees):
        position = int(degrees * self.motor.position.positions / 360)
        return position

    @Log.method(level=4)
    def relative_to_steps(self, degrees):
        steps = int(degrees * self.motor.position.positions / 360)
        return steps

    @Log.method(logging.INFO)
    def relative(self, degrees):
        relative_steps = self.degrees_to_position(degrees)
        self.motor.steps(relative_steps)

    @Log.method(logging.INFO)
    def absolute(self, degrees, direction=None):
        target = self.degrees_to_position(degrees)
        relative_steps = self.motor.position.absolute_to_relative(target, direction)
        self.motor.steps(relative_steps)
