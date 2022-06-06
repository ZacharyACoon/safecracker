import time
import asyncio

class IndexedMotorWrapper:
    def __init__(self, degree_motor, photointerrupter, photointerrupter_degrees):
        self.dm = degree_motor
        self.pi = photointerrupter
        self.pip = photointerrupter_degrees

    def find_index(self, direction=False):
        degrees = (1 if direction else -1) * 360
        list(self.dm.relative(degrees))
        for step in self.dm.relative(degrees):
            if self.pi.status():
                print("Found index.")
                if self.dm.degrees != self.pip:
                    print(f"We thought we were at {self.dm.degrees}.  Truing to {self.pip}.")
                    self.dm.degrees = self.pip
                    return 2
                else:
                    return 1
        return 0

class DialMotorWrapper:
    def __init__(self, degree_motor, numbers, left_to_right=True):
        self.motor = degree_motor
        self.numbers = numbers
        self.left_to_right = left_to_right
        self.number = 0

    def convert_number_to_absolute_degrees(self, number):
        absolute_degrees = 360 / self.numbers * number
        absolute_degrees *= -1 if self.left_to_right else 1
        return absolute_degrees

    def absolute(self, number, direction=False):
        degrees = self.convert_number_to_absolute_degrees(number)
        yield from self.motor.absolute(degrees, direction)
