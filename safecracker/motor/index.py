from safecracker.log import Log
import RPi.GPIO as g
import time
import logging


class ToleranceException(Exception):
    pass

class NotFoundException(Exception):
    pass


class Index(Log):
    def __init__(self, motor, pin, position_degrees, tolerance_degrees=0.1, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.motor = motor
        self.pin = pin
        self.degrees = position_degrees
        self.tolerance_degrees = tolerance_degrees
        g.setup(self.pin, g.IN)
        self.last_status = None
        self._calibrate = False

    @Log.method(1)
    def status(self):
        return bool(g.input(self.pin))

    @Log.method(3)
    def _check_for_left_edge(self):
        status = self.status()
        direction = self.motor.driver.direction
        position = self.motor.position.position
        positions = self.motor.position.positions

        left = None
        if direction and self.last_status is False and status:
            left = position
        elif not direction and self.last_status is True and not status:
            left = (position + 1) % positions
        self.last_status = status

        if left:
            left_degrees = left * 360 / positions
            difference = abs(self.degrees - left_degrees)
            self.log.debug(f"position={left}, degrees={left_degrees}.  Expected degrees={self.degrees}.  Difference={round(difference, 4)}.  Tolerance={self.tolerance_degrees}")
            if self._calibrate or difference > self.tolerance_degrees:
                raise ToleranceException(f"Difference {round(difference, 4)}>{self.tolerance_degrees}")

    @Log.method(4)
    def step(self):
        self._check_for_left_edge()

    @Log.method(logging.INFO)
    def calibrate(self, direction=None):
        self._calibrate = True
        try:
            self.motor.degrees.relative(360 * (1 if direction else -1))
            raise NotFoundException("Index not found?")
        except ToleranceException as e:
            self._calibrate = False
            self.motor.position.position = int(self.degrees * self.motor.position.positions / 360)
            self.log.warning("Calibrated position.")
