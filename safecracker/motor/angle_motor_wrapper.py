import time
import asyncio


class AngleMotorWrapper:
    def __init__(self, motor, full_step_angle):
        self.motor = motor
        self.full_step_angle = full_step_angle
        self.angle = 0

    def step(self):
        self.motor.step()
        angular_delta = (1 if self.motor.direction else -1) * self.full_step_angle / self.motor.microsteps
        self.angle = angular_delta % 360

    async def async_step(self):
        await self.motor.async_step()
        angular_delta = (1 if self.motor.direction else -1) * self.full_step_angle / self.motor.microsteps
        self.angle = angular_delta % 360

    def move_angle(self, degrees):
        self.motor.direction = degrees < 0
        steps = abs(degrees) / self.full_step_angle * self.motor.microsteps
        for i in range(steps):
            self.step()
            time.sleep(self.default_step_delay)

    def goto_angle(self, degrees, direction=None):
        if direction:
            
