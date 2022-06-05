from safecracker.sensors.photointerrupter import Photointerrupter
from safecracker.motor.a4988 import A4988_Pins, A4988
from safecracker.motor.angle_motor_wrapper import AngleMotorWrapper
from safecracker.motor.indexed_motor_wrapper import IndexedMotorWrapper
from safecracker.motor.acceleration_motor_wrapper import AccelerationMotorWrapper
from mpu6050 import mpu6050

import time
import asyncio


class Safecracker:
    def __init__(self, config, acceleration_profile):
        self.config = config
        self.pi = Photointerrupter(self.config["hardware"]["photointerrupter"]["pin"])
        self.ag = mpu6050(self.config["hardware"]["accelerometer_gyroscope"]["i2c_address"])

        self.m = A4988(A4988_Pins(**self.config["hardware"]["a4988_pins"]))
        self.anm = AngleMotorWrapper(self.m, self.config["hardware"]["motor"]["full_step_angle"])
        self.acm = AccelerationMotorWrapper(self.anm, default_acceleration_profile=acceleration_profile)
        self.im = IndexedMotorWrapper(self.anm, self.acm, self.pi, self.config["hardware"]["photointerrupter"]["angle"])

    def index(self):
        """Find the Angle which activates the photointerrupter.  This will likely interfere with the entered combination of the safe."""
        self.m.hold()
        steps = int((360 / self.anm.full_step_angle) * self.m.microsteps)
        for i in range(steps):
            self.anm.step()
            time.sleep(self.m.default_step_delay)
            if self.pi.status():
                angle_outside_tolerance_bool = abs(self.anm.angle - self.config["hardware"]["photointerrupter"]["angle"]) > self.config["hardware"]["motor"]["tolerance_angle"]
                self.anm.angle = self.config["hardware"]["photointerrupter"]["angle"]
                if angle_outside_tolerance_bool:
                    print("Tracked angle wrong.  Truing.")
                return angle_outside_tolerance_bool

    async def async_index(self):
        self.m.hold()
        steps = int((360 / self.anm.full_step_angle) * self.m.microsteps)
        for i in range(steps):
            self.anm.step()
            await asyncio.sleep(self.m.default_step_delay)
            if self.pi.status():
                angle_outside_tolerance_bool = abs(self.anm.angle - self.config["hardware"]["photointerrupter"]["angle"]) > self.config["hardware"]["motor"]["tolerance_angle"]
                self.anm.angle = self.config["hardware"]["photointerrupter"]["angle"]
                if angle_outside_tolerance_bool:
                    print("Tracked angle wrong.  Truing.")
                return angle_outside_tolerance_bool

    def zero(self):
        self.anm.target_angle(0)
