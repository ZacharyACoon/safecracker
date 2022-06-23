import RPi.GPIO as g
from collections import namedtuple
import time
import trio
import logging
from safecracker.log import Log

# This stepper driver class should be able to control a stepper driver via a a4988 stepper driver board.
# direction, step, microsteps defined in binary (ms1, ms2, ms3), and enable which allows spinning freely.
A4988_Pins = namedtuple("A4988Pins", ['direction', 'step', 'ms1', 'ms2', 'ms3', 'enable'])


class A4988(Log):
    _microsteps_to_pin_state_map = {
        1: (0, 0, 0),
        2: (1, 0, 0),
        4: (0, 1, 0),
        8: (1, 1, 0),
        16: (1, 1, 1)
    }
    default_step_delay = 0.05

    def __init__(self, a4988_pins, microsteps=4, step_delay=None, parent_logger=None):
        super().__init__(parent_logger)
        self.a4988_pins = a4988_pins
        for pin in self.a4988_pins:
            g.setup(pin, g.OUT)
            g.output(pin, 0)

        self.engaged = True
        self.direction = True
        self.microsteps = microsteps
        self.step_delay = step_delay or self.default_step_delay

    @property
    def direction(self):
        return self._direction

    @direction.setter
    @Log.method
    def direction(self, d: bool):
        d = bool(d)
        g.output(self.a4988_pins.direction, int(not d))
        self._direction = d

    @property
    def microsteps(self):
        return self._microsteps

    @microsteps.setter
    @Log.method
    def microsteps(self, m: int):
        assert m in self._microsteps_to_pin_state_map
        pins = self.a4988_pins.ms1, self.a4988_pins.ms2, self.a4988_pins.ms3
        for i, v in enumerate(self._microsteps_to_pin_state_map[m]):
            g.output(pins[i], v)
        self._microsteps = m

    @property
    def engaged(self):
        return self._engaged

    @engaged.setter
    @Log.method
    def engaged(self, e: bool):
        g.output(self.a4988_pins.enable, int(not e))
        self._engaged = e

    @Log.method(level=3)
    def step(self):
        g.output(self.a4988_pins.step, 1)
        time.sleep(1/1000000)
        g.output(self.a4988_pins.step, 0)

    @Log.method
    def steps(self, delta):
        self.direction = delta > 0
        for _ in range(abs(delta)):
            self.step()
            time.sleep(self.default_step_delay / self.microsteps)

    @property
    def step_delay(self):
        return self.default_step_delay

    @step_delay.setter
    def step_delay(self, v):
        self.default_step_delay = v
