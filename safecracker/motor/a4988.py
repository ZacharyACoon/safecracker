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

    def __init__(self, a4988_pins, microsteps_per_step=4, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.a4988_pins = a4988_pins
        for pin in self.a4988_pins:
            g.setup(pin, g.OUT)
            g.output(pin, 0)

        self._microsteps = microsteps_per_step
        self._engaged = False
        self._direction = False
        self.direction = False
        self.microsteps = microsteps_per_step

    @property
    def engaged(self):
        return self._engaged

    @engaged.setter
    @Log.method(8)
    def engaged(self, e: bool):
        g.output(self.a4988_pins.enable, int(not e))
        self._engaged = e

    @property
    def direction(self):
        return self._direction

    @direction.setter
    @Log.method(8)
    def direction(self, d: bool):
        d = bool(d)
        g.output(self.a4988_pins.direction, int(not d))
        self._direction = d

    @property
    def microsteps(self):
        return self._microsteps

    @microsteps.setter
    @Log.method(8)
    def microsteps(self, m: int):
        assert m in self._microsteps_to_pin_state_map
        pins = self.a4988_pins.ms1, self.a4988_pins.ms2, self.a4988_pins.ms3
        for i, v in enumerate(self._microsteps_to_pin_state_map[m]):
            g.output(pins[i], v)
        self._microsteps = m

    @Log.method(4)
    def step(self):
        g.output(self.a4988_pins.step, 1)
        time.sleep(1/1000000)
        g.output(self.a4988_pins.step, 0)
