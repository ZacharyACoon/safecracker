from safecracker.log import Log
import RPi.GPIO as g
import time


class OutOfToleranceError(Exception):
    pass

class IndexNotFoundError(Exception):
    pass


class Index(Log):
    def __init__(self, motor, pin, position_degrees, tolerance_degrees=0.1, parent_logger=None, parent=None):
        super().__init__(parent_logger, parent)
        self.motor = motor
        self.pin = pin
        self.position_degrees = position_degrees
        self.tolerance_degrees = 0.1
        g.setup(self.pin, g.IN)
        self.last_status = None

    @Log.method(1)
    def status(self):
        return bool(g.input(self.pin))

    @Log.method(4)
    def _check_for_left_edge(self):
        status = self.status()
        direction = self.motor.driver.direction
        position = self.motor.position.position
        positions = self.motor.position.positions

        left = None
        if not direction and not self.last_status and status:
            left = position
        elif direction and self.last_status and not status:
            left = (position + 1) % positions
        if left:
            left_degrees = position * 360 / positions
            difference = abs(self.position_degrees - left_degrees)
            if difference > self.tolerance_degrees:
                # out of tolerance
                raise OutOfToleranceError(f"Found at: {left_degrees}, Difference: {difference}>{self.tolerance_degrees}")
        self.last_status = status

    @Log.method(2)
    def step(self):
        self._check_for_left_edge()

    @Log.method
    def calibrate(self, direction=None):
        try:
            print("here?")
            self.motor.degrees.relative(360 * (1 if direction else -1))
        except OutOfToleranceError as e:
            self.motor.position.position = int(self.position_degrees * self.motor.position.positions / 360)
