from safecracker.sensors.photointerrupter import Photointerrupter
from safecracker.motor.a4988 import A4988_Pins, A4988
from safecracker.motor.degree_motor_wrapper import DegreeMotorWrapper
from safecracker.motor.indexed_motor_wrapper import IndexedMotorWrapper
from safecracker.motor.acceleration_motor_wrapper import AccelerationMotorWrapper
from mpu6050 import mpu6050

import time
import asyncio


class Safecracker:
    def __init__(self, config):
        self.config = config
        self.pi = Photointerrupter(self.config["hardware"]["photointerrupter"]["pin"])
        self.ag = mpu6050(self.config["hardware"]["accelerometer_gyroscope"]["i2c_address"])

        self.m = A4988(A4988_Pins(**self.config["hardware"]["a4988_pins"]))
        self.dm = DegreeMotorWrapper(self.m, self.config["hardware"]["motor"]["full_step_degrees"])
        self.im = IndexedMotorWrapper(self.dm, self.pi, self.config["hardware"]["photointerrupter"]["degrees"])

    def find_index(self, direction=False):
        self.im.find_index(direction)

    def zero(self, direction=False):
        list(self.dm.absolute(0, direction))

    def wipe(self, direction=False):
        list(self.dm.relative((1 if direction else -1) * -4*360))
