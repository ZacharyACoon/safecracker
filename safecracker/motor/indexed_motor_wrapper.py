import time
import asyncio


class IndexedMotorWrapper:
    def __init__(self, degree_motor, photointerrupter, photointerrupter_degrees):
        self.dm = degree_motor
        self.pi = photointerrupter
        self.pip = photointerrupter_degrees

    def find_index(self, direction=False):
        degrees = (1 if direction else -1) * 360
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
