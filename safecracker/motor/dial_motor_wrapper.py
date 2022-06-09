import time
import asyncio


class DialMotorWrapper:
    def __init__(self, degree_motor, numbers, left_to_right=True):
        self.motor = degree_motor
        self.numbers = numbers
        self.left_to_right = left_to_right
        self.number = 0

    def convert_number_to_absolute_degrees(self, number):
        absolute_degrees = 360 / self.numbers * number
        if self.left_to_right:
            absolute_degrees = 360 - absolute_degrees
        #absolute_degrees *= -1 if self.left_to_right else 1
        return absolute_degrees

    def absolute(self, number, direction=False):
        degrees = self.convert_number_to_absolute_degrees(number)
        yield from self.motor.absolute(degrees, direction)
