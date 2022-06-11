import time
import asyncio


class IndexedMotorWrapper:
    def __init__(self, degree_motor, photointerrupter, photointerrupter_degrees, tolerance_degrees=0.1):
        self.motor = degree_motor
        self.pi = photointerrupter
        self.pip = photointerrupter_degrees
        self.tolerance_degrees = tolerance_degrees

    def find_index(self, direction=False):
        a = b = None
        for _ in self.motor.relative((-1 if direction else 1) * 405):
            # find beginning of index
            if self.pi.status() and a is None:
                a = self.motor.degrees
            # find end of index
            elif not self.pi.status() and a is not None and b is None:
                b = self.motor.degrees

                if direction:
                    if a > b:
                        width = a - b
                    else:
                        width = 360 - b + a
                else:
                    if b > a:
                        width = b - a
                    else:
                        width = 360 - a + b

                center = width / 2
                index_degrees = self.pip + (-center if direction else center)
                print(f"Direction={direction}, a={a}, b={b}, w={width}, c={center}")
                if abs(self.pip - index_degrees) > self.tolerance_degrees:
                    print(f"Current position was {index_degrees}.  Truing to {self.pip}.")
                    self.motor.degrees = index_degrees
                    break
        else:
            print("Not found?")

    async def async_find_index(self, direction=False):
        direction = -1 if direction else 1
        a = b = None
        for _ in self.motor.async_relative(direction * 360):
            # find beginning of index
            if self.pi.status() and on is None:
                a = self.motor.degrees
            # find end of index
            elif not self.pi.status() and a is not None and b is None:
                b = self.motor.degrees
                if direction and b > a:
                    width = 360 - b + a
                elif not direction and a > b:
                    width = 360 - a + b
                center = width / 2
                print(f"Width={width}")
                index_degrees = self.pip + center
                if abs(index_degrees - self.pip) > self.tolerance_degrees:
                    print(f"Current position was {index_degrees}.  Truing to {self.pip}.")
                    self.motor.degrees = index_degrees
                    break
