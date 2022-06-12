from safecracker.sensors.photointerrupter import Photointerrupter
from safecracker.motor.a4988 import A4988_Pins, A4988
from safecracker.motor.degree_motor_wrapper import DegreeMotorWrapper
from safecracker.motor.indexed_motor_wrapper import IndexedMotorWrapper
from safecracker.motor.dial_motor_wrapper import DialMotorWrapper
from mpu6050 import mpu6050

import time
import asyncio


class Safecracker:
    def __init__(self, config):
        self.config = config
        self.pi = Photointerrupter(self.config["hardware"]["photointerrupter"]["pin"])
        #self.ag = mpu6050(self.config["hardware"]["accelerometer_gyroscope"]["i2c_address"])

        self.motor = A4988(A4988_Pins(**self.config["hardware"]["a4988_pins"]))
        self.degree_motor_wrapper = DegreeMotorWrapper(
            self.motor,
            self.config["hardware"]["motor"]["full_step_degrees"]
        )
        self.indexed_motor_wrapper = IndexedMotorWrapper(
            self.degree_motor_wrapper,
            self.pi,
            self.config["hardware"]["photointerrupter"]["degrees"]
        )
        self.dial_motor_wrapper = DialMotorWrapper(
            self.degree_motor_wrapper,
            self.config["hardware"]["dial"]["numbers"],
            self.config["hardware"]["dial"]["tolerance"],
            left_to_right=self.config["hardware"]["dial"]["left_to_right"]
        )

    def find_index(self, direction=None):
        self.indexed_motor_wrapper.find_index(direction)

    def zero(self, direction=None):
        list(self.degree_motor_wrapper.absolute(0, direction))

    def wipe(self, direction=False):
        list(self.degree_motor_wrapper.relative((-1 if direction else 1) * 4*360))

    def index_to_combination(self, base, v):
        c1, v = divmod(v, base*base)
        c2, c3 = divmod(v, base)
        return c1, c2, c3

    def iterate_through_combinations(self, start=0):
        numbers = self.dial_motor_wrapper.numbers
        tolerance = self.dial_motor_wrapper.tolerance
        scaled_dial_range = numbers // tolerance
        combination_count = scaled_dial_range ** 3
        latch_degrees = self.config["hardware"]["dial"]["latch_degrees"]

        self.find_index(direction=True)
        self.zero(direction=True)

        a = start
        while a < combination_count:
            scs = self.index_to_combination(scaled_dial_range, a)
            c1, c2, c3 = tuple(v*tolerance for v in scs)
            print(f"Attempt={a}, Combination={(c1, c2, c3)}")

            # c1
            list(self.degree_motor_wrapper.relative(-360*3))
            list(self.dial_motor_wrapper.absolute(c1, direction=True))
            time.sleep(0.1)

            # c2
            list(self.degree_motor_wrapper.relative(360*2))
            list(self.dial_motor_wrapper.absolute(c2, direction=False))
            time.sleep(0.1)

            # try c3s rapidly.
            list(self.degree_motor_wrapper.relative(-360))
            while c3 < numbers:
                if c3 != 0:
                    print(f"Attempt={a}, Combination={c1, c2, c3}")

                # c3
                list(self.dial_motor_wrapper.absolute(c3, direction=True))
                time.sleep(0.1)

                # attempt to latch
                list(self.degree_motor_wrapper.relative(latch_degrees))
                # return
                list(self.degree_motor_wrapper.relative(-latch_degrees))

                c3 += tolerance
                a += 1

            # finished a range
            # test if we're off.
            result = self.indexed_motor_wrapper.find_index(direction=True)
            yield result, a
