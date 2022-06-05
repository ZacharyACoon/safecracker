import time
import asyncio


class IndexedMotorWrapper:
    def __init__(self, position_motor, acceleration_motor, photointerrupter, photointerrupter_position):
        self.pm = position_motor
        self.am = acceleration_motor
        self.pi = photointerrupter
        self.pip = photointerrupter_position

    def find_index(self):
        def step_callback():
            print("sc")
            if self.pi.status():
                print(f"Found index at position {self.pm}")

        self.am.steps(200*self.pm.motor.microsteps, step_callback=step_callback)
