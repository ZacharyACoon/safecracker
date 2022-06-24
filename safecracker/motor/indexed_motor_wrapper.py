from safecracker.log import Log
import RPi.GPIO as g
import time


class IndexedMotorWrapper(Log):
    def __init__(self, degrees_motor_wrapper, pin, degrees, tolerance=0.1, parent_logger=None):
        super().__init__(parent_logger)

        self.degrees_motor_wrapper = degrees_motor_wrapper
        self.pin = pin
        self.degrees = degrees
        self.tolerance = int(tolerance * self.degrees_motor_wrapper.scaler)


        self.scaled_degrees = int(degrees * self.degrees_motor_wrapper.scaler)
        g.setup(self.pin, g.IN)
        self.degrees_left = 0
        self.degrees_right = 0

    @Log.method(1)
    def status(self):
        return bool(g.input(self.pin))

    @Log.method(2)
    def _check_for_edge(self, direction, left, right):
        status = self.status()
        degrees = self.degrees_motor_wrapper._scaled_degrees
        if direction and status:
            if not right:
                right = degrees
            left = degrees
        elif not direction and status:
            if not left:
                 left = degrees
            right = degrees
        finished = bool(left is not None and right is not None and not status)
        return finished, left, right

    @Log.method(3)
    def find_edges(self, direction=None):
        while self.status():
            self.degrees_motor_wrapper.step()

        left = None
        right = None
        self.degrees_motor_wrapper.motor.direction = direction
        for _ in range(self.degrees_motor_wrapper.relative_to_steps(360)):
            self.degrees_motor_wrapper.step()
            time.sleep(self.degrees_motor_wrapper.motor.default_step_delay / self.degrees_motor_wrapper.motor.microsteps)
            finished, left, right = self._check_for_edge(direction, left, right)
            if finished and left is not None and right is not None:
                self.log.debug("Found index.")
                break
        else:
            raise Exception("Index not found.")

        return left, right


    @Log.method(level=5)
    def find(self, direction=False):
        left, right = self.find_edges(direction=direction)
        s = self.degrees_motor_wrapper.scaler

        # determine width of sensor
        if direction:
            if left >= right:
                width = (right + (s*360)) - left
            else:
                width = right - left
        else:
            if right >= left:
                width = (s*360) - right + left
            else:
                width = right - left

        distance_to_center = int(width / 2)
        # center of sensor
        center = (left + distance_to_center) % (360 * self.degrees_motor_wrapper.scaler)
        last_position = left if direction else right
        return left, right, center, distance_to_center, last_position

    @Log.method
    def calibrate(self, direction=None):
        left, right, center, distance_to_center, last_position = self.find(direction=direction)
        s = self.degrees_motor_wrapper.scaler
        self.degrees_motor_wrapper._scaled_degrees = self.degrees * self.degrees_motor_wrapper.scaler + (-distance_to_center if direction else distance_to_center)

    @Log.method
    def check_calibration(self, direction=None):
        left, right, center, distance_to_center, last_position = self.find(direction=direction)
        center /= self.degrees_motor_wrapper.scaler
        difference = abs(center - self.degrees)
        within_tolerance = difference < self.tolerance
        self.log.warning(f"calibration within_tolerance={within_tolerance}, difference={difference}")
        return within_tolerance, difference
