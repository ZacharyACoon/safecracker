import time
import asyncio


class DegreeMotorWrapper:
    def __init__(self, motor, full_step_degrees):
        self.motor = motor
        self.full_step_degrees = full_step_degrees
        self.degrees = 0

    def step(self):
        self.motor.step()
        angular_delta = (1 if self.motor.direction else -1) * self.full_step_degrees / self.motor.microsteps
        self.degrees = angular_delta % 360

    def steps(self, count):
        self.motor.set_direction(count > 0)
        for _ in range(abs(count)):
            self.step()
            time.sleep(self.motor.default_step_delay)
            yield

    def relative(self, degrees):
        self.motor.direction = degrees < 0
        steps = int(abs(degrees) / self.full_step_degrees * self.motor.microsteps)
        yield from self.steps(steps)

    def determine_degrees_to_absolute(self, absolute_degrees, direction=None):
        left = absolute_degrees + (360 if absolute_degrees < self.degrees else 0) - self.degrees
        right = absolute_degrees - (360 if absolute_degrees > self.degrees else 0) - self.degrees
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

    def absolute(self, absolute_degrees, direction=None):
        relative_degrees = self.determine_degrees_to_absolute(absolute_degrees, direction)
        yield from self.relative(relative_degrees)

    async def async_step(self):
        await self.motor.async_step()
        angular_delta = (1 if self.motor.direction else -1) * self.full_step_degrees / self.motor.microsteps
        self.degrees = angular_delta % 360

    async def async_steps(self, count):
        self.motor.set_direction(count > 0)
        for _ in range(abs(count)):
            await self.async_step()
            await asyncio.sleep(self.motor.default_step_delay)
            yield
