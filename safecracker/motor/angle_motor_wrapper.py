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

    def determine_angular_distance_to_target(self, angle, direction=None):
        left = angle + (360 if angle < self.angle else 0) - self.angle
        right = angle - (360 if angle > self.angle else 0) - self.angle
        print(left, right)
        if direction is True:
            return right
        elif direction is False:
            return left
        else:
            if abs(left) < abs(right):
                return left
            else:
                return right

    def target_angle(self, target_angle, direction=None):
        target_degrees_delta = self.determine_angular_distance_to_target(target_angle, direction)
        self.motor.direction = target_angle < 0
        print(self.full_step_angle, self.motor.microsteps)
        steps = int(abs(target_degrees_delta) / self.full_step_angle * self.motor.microsteps)
        for i in range(steps):
            self.step()
            time.sleep(self.motor.default_step_delay)
