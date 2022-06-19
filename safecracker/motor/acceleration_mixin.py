import time
import asyncio


class AccelerationMotorWrapper:
    def __init__(self, motor, default_acceleration_profile):
        self.motor = motor
        self.default_acceleration_profile = default_acceleration_profile

    def steps(self, count, acceleration_profile=None, step_callback=False):
        print(step_callback)
        acceleration_profile = acceleration_profile or self.default_acceleration_profile
        for i in range(count):
            d = acceleration_profile(i, count)
            print(i, count, d)
            self.motor.step()
            if i != count - 1:
                time.sleep(d)
            if step_callback:
                step_callback()

    async def async_steps(self, count, acceleration_profile):
        for i in range(count):
            await self.motor.step()
            await asyncio.sleep(acceleration_profile)
