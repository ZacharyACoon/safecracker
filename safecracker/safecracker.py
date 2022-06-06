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
        self.degree_motor_wrapper = DegreeMotorWrapper(self.motor, self.config["hardware"]["motor"]["full_step_degrees"])
        self.indexed_motor_wrapper = IndexedMotorWrapper(self.degree_motor_wrapper, self.pi, self.config["hardware"]["photointerrupter"]["degrees"])
        self.dial_motor_wrapper = DialMotorWrapper(self.degree_motor_wrapper, config["hardware"]["dial"]["numbers"])

    def find_index(self, direction=False):
        self.indexed_motor_wrapper.find_index(direction)

    def zero(self, direction=False):
        list(self.degree_motor_wrapper.absolute(0, direction))

    def wipe(self, direction=False):
        list(self.degree_motor_wrapper.relative((1 if direction else -1) * -4*360))

    def first_two_numbers(self, c1, c2):
        self.wipe()
