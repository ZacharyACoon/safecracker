import RPi.GPIO as g
import time
from collections import namedtuple
from contextlib import contextmanager
import trio


# This stepper driver class should be able to control a stepper driver via a a4988 stepper driver board.
# direction, step, microsteps defined in binary (ms1, ms2, ms3), and enable which allows spinning freely.
A4988_Pins = namedtuple("A4988Pins", ['direction', 'step', 'ms1', 'ms2', 'ms3', 'enable'])


class A4988:
    microsteps_to_pin_states = {
        1: (0, 0, 0),
        2: (1, 0, 0),
        4: (0, 1, 0),
        8: (1, 1, 0),
        16: (1, 1, 1)
    }
    default_pulse_width = 1/1000000
    default_step_delay = 0.001

    def __init__(self, a4988_pins, microsteps=4, default_step_delay=None):
        self.pins = a4988_pins
        for pin in self.pins:
            g.setup(pin, g.OUT)
            g.output(pin, 0)

        self.direction = False
        self.microsteps = 1
        self.set_microsteps(microsteps)
        self.default_step_delay = default_step_delay or self.default_step_delay

    def set_microsteps(self, microsteps):
        assert microsteps in self.microsteps_to_pin_states
        self.microsteps = microsteps
        microstep_pins = self.pins.ms1, self.pins.ms2, self.pins.ms3
        for i, value in enumerate(self.microsteps_to_pin_states[self.microsteps]):
            g.output(microstep_pins[i], value)

    def free(self):
        g.output(self.pins.enable, 1)

    def hold(self):
        g.output(self.pins.enable, 0)

    def set_direction(self, direction: bool):
        g.output(self.pins.direction, int(direction))

    def step(self):
        g.output(self.pins.step, 1)
        time.sleep(self.default_pulse_width)
        g.output(self.pins.step, 0)

    def steps(self, count):
        self.set_direction(count < 0)
        for _ in range(abs(count)):
            self.step()
            time.sleep(self.default_step_delay)
            yield

    async def async_step(self):
        g.output(self.pins.step, 1)
        await trio.sleep(self.default_pulse_width)
        g.output(self.pins.step, 0)

    async def async_steps(self, count):
        self.set_direction(count < 0)
        for _ in range(abs(count)):
            await self.async_step()
            await trio.sleep(self.default_step_delay)
            yield
