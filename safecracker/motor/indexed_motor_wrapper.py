import time
import asyncio


class IndexedMotorWrapper:
    def __init__(self, degree_motor, photointerrupter, photointerrupter_degrees):
        self.dm = degree_motor
        self.pi = photointerrupter
        self.pip = photointerrupter_degrees

    def find_index(self, direction=False):
        direction = 1 if direction else -1
        list(self.dm.relative(direction * 360))
        for step in self.dm.relative(direction * 360):
            if self.pi.status():
                print("Found index.")
                if self.dm.degrees != self.pip:
                    print(f"We thought we were at {self.dm.degrees}.  Truing to {self.pip}.")
                    self.dm.degrees = self.pip
                    return 2
                else:
                    return 1
        return 0

    async def async_find_index(self, direction=False):
        directoin = 1 if direction else -1
        async for step in self.dm.async_relative(direction * 360):
            if self.pi.status():
                print("Found index.")
                if self.dm.degrees != self.pip:
                    print(f"We thought we were at {self.dm.degrees}.  Truing to {self.pip}.")
                    self.dm.degrees = self.pip
                    return 2
                else:
                    return 1
        return 1
