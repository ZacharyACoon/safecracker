import time
import trio
import unittest


class DegreeMotorWrapper:
    def __init__(self, motor, full_step_degrees):
        self.motor = motor
        self.full_step_degrees = full_step_degrees
        self.degrees = 0

    def step(self):
        self.motor.step()
        step_angle = (-1 if self.motor.direction else 1) * self.full_step_degrees / self.motor.microsteps
        self.degrees += step_angle
        self.degrees %= 360

    def steps(self, count):
        self.motor.set_direction(count < 0)
        for _ in range(abs(count)):
            self.step()
            time.sleep(self.motor.default_step_delay)
            yield

    def relative(self, degrees):
        steps = int((degrees / self.full_step_degrees) * self.motor.microsteps)
        print(f"    d={degrees}/fsdegrees={self.full_step_degrees} * ms={self.motor.microsteps} => s={steps}")
        yield from self.steps(steps)

    def absolute_to_relative(self, target_degrees, direction=None):
        p = self.degrees
        t = target_degrees % 360
        if t == p:
            left = 0
            right = 0
        elif t < p:
            left = t - p
            right = 360 - p + t
        else:
            left = -360 - p + t
            right = t - p
        #print(f"    D={direction}, P={p}, T={t}, L={left}, R={right}")

        # TRUE IS CLOCKWISE
        if direction is False:
            return right
        elif direction is True:
            return left
        elif direction is None:
            if abs(left) < abs(right):
                return left
            else:
                return right

    def absolute(self, absolute_degrees, direction=None):
        relative_degrees = self.absolute_to_relative(absolute_degrees, direction)
        #print(f"relative={relative_degrees}")
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
        relative_degrees = self.absolute_to_relative(absolute_degrees, direction)
        async for _ in self.async_relative(relative_degrees):
            yield


class TestDegreeMotor(unittest.TestCase):
    def test1_absolute_to_relative(self):
        self.motor = DegreeMotorWrapper({"microsteps": 16}, 1.8)

        print("Right")
        for i in range(90, 360, 90):
            r = self.motor.absolute_to_relative(i, direction=False)
            self.assertEqual(90, r)
            self.motor.degrees += r

        self.motor.degrees = 0
        print("Left")
        for i in range(-90, -360, -90):
            r = self.motor.absolute_to_relative(i, direction=True)
            self.assertEqual(-90, r)
            self.motor.degrees += r
            self.motor.degrees %= 360
