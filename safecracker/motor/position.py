from safecracker.log import Log
import time
import unittest


class Position(Log):
    def __init__(self, motor, positions, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.motor = motor
        self.positions = positions
        self.position = 0

    @Log.method(4)
    def step(self):
        self.position = (self.position + (1 if self.motor.driver.direction else -1)) % self.positions

    @Log.method(11, log_return=True)
    def absolute_to_relative(self, target, direction=None):
        p = self.position
        t = target % self.positions
        if t == p:
            left = -self.positions
            right = self.positions
        elif t < p:
            left = t - p
            right = self.positions + left
        elif t > p:
            right = t - p
            left = right - self.positions

        #print(f"p={p}, t={t}, l={left}, r={right}")

        if direction is False:
            return left
        elif direction is True:
            return right
        else:
            if abs(left) <= abs(right):
                return left
            else:
                return right


class Test1(unittest.TestCase):
    def test1_right_0_800(self):
        a = Position(None, 3200)
        a.position = 0
        r = a.absolute_to_relative(800, True)
        self.assertEqual(r, 800)

    def test2_left_800_0(self):
        a = Position(None, 3200)
        a.position = 800
        r = a.absolute_to_relative(0, False)
        self.assertEqual(r, -800)

    def test3_left_800_2400(self):
        a = Position(None, 3200)
        a.position = 800
        r = a.absolute_to_relative(2400, False)
        self.assertEqual(r, -1600)

    def test4_right_800_2400(self):
        a = Position(None, 3200)
        a.position = 800
        r = a.absolute_to_relative(2400, True)
        self.assertEqual(r, 1600)
