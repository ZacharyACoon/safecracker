import time
import trio


class DegreeMotorWrapper:
    def __init__(self, motor, full_step_degrees):
        self.motor = motor
        self.full_step_degrees = full_step_degrees
        self.degrees = 0

    def step(self):
        self.motor.step()
        angular_delta = (1 if self.motor.direction else -1) * self.full_step_degrees / self.motor.microsteps
        self.degrees += angular_delta
        self.degrees %= 360

    def steps(self, count):
        self.motor.set_direction(count < 0)
        for _ in range(abs(count)):
            self.step()
            time.sleep(self.motor.default_step_delay)
            yield

    def relative(self, degrees):
        steps = int(degrees / self.full_step_degrees * self.motor.microsteps)
        yield from self.steps(steps)

    def determine_degrees_to_absolute(self, target_degrees, direction=None):
        p = self.degrees
        t = target_degrees % 360
        if t < p:
            left = t - p
            right = 360 - p + t
        else:
            left = t - 360 - p
            right = t - p
        print(p, t, left, right)

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
        print("moving", relative_degrees)
        yield from self.relative(relative_degrees)

    async def async_step(self):
        await self.motor.async_step()
        angular_delta = (1 if self.motor.direction else -1) * self.full_step_degrees // self.motor.microsteps
        self.degrees = angular_delta % 360

    async def async_steps(self, count):
        self.motor.set_direction(count < 0)
        for _ in range(abs(count)):
            await self.async_step()
            await trio.sleep(self.motor.default_step_delay)
            yield

    async def async_relative(self, degrees):
        steps = int(degrees // self.full_step_degrees * self.motor.microsteps)
        async for _ in self.async_steps(steps):
            yield

    async def async_absolute(self, absolute_degrees, direction=None):
        relative_degrees = self.determine_degrees_to_absolute(absolute_degrees, direction)
        async for _ in self.async_relative(relative_degrees):
            yield
