import time
import asyncio


class IndexedMotorWrapper:
    def __init__(self, degree_motor, photointerrupter, photointerrupter_degrees, tolerance_degrees=0.1):
        self.motor = degree_motor
        self.pi = photointerrupter
        self.pip = photointerrupter_degrees
        self.tolerance_degrees = tolerance_degrees

    def find_index(self, direction=True):
        direction = -1 if direction else 1
        on = None
        off = None
        for step in self.motor.relative(direction * 360):
            # find beginning of index
            if self.pi.status() and on is None:
                on = self.motor.degrees
                print("On", on)
            # find end of index
            elif not self.pi.status() and on is not None and off is None:
                off = self.motor.degrees
                width = abs(on - off)
                center = width / 2
                print(f"Off={off}, Width={width}, Center={center}")
                index_degrees = self.pip + (-center if direction else center)
                if abs(index_degrees - self.pip) > self.tolerance_degrees:
                    print(f"Current position was {index_degrees}.  Truing to {self.pip}.")
                    self.motor.degrees = index_degrees
                    break
        else:
            print("Not found?")

    async def async_find_index(self, direction=False):
        direction = -1 if direction else 1
        on = None
        off = None
        for step in self.motor.async_relative(direction * 360):
            # find beginning of index
            if self.pi.status() and on is None:
                on = self.motor.degrees
            # find end of index
            elif not self.pi.status() and on is not None and off is None:
                off = self.motor.degrees
                width = abs(on - off)
                center = width / 2
                print(f"Width={width}")
                index_degrees = self.pip + (-center if direction else center)
                if abs(index_degrees - self.pip) > self.tolerance_degrees:
                    print(f"Current position was {index_degrees}.  Truing to {self.pip}.")
                    self.motor.degrees = index_degrees
                    break
