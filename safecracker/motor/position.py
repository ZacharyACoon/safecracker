from safecracker.log import Log
import time


class Position(Log):
    def __init__(self, motor, positions, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.motor = motor
        self.positions = positions
        self.position = 0

    @Log.method(2)
    def step(self):
        self.position = (self.position + (1 if self.motor.driver.direction else -1)) % self.positions

    def absolute_to_relative(self, target, direction=None):
        p = self.position
        t = target

        if t == p:
            left = -self.positions
            right = self.positions
        elif t < p:
            left = t - p
            right = self.positions + left
        elif t > p:
            left = p - t
            right = self.positions + left

        if direction is False:
            return left
        elif direction is True:
            return right
        else:
            if abs(left) <= right:
                return left
            else:
                return right
