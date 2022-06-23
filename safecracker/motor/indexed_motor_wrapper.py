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

    @Log.method(3)
    def status(self):
        return bool(g.input(self.pin))

    def _check_for_edge(self, direction, left, right):
        status = self.status()
        degrees = self.degrees_motor_wrapper._scaled_degrees
        if direction and status:
            if not left:
                left = degrees
            right = degrees
        elif not direction and status:
            if not right:
                right = degrees
            left = degrees
        finished = left and right and not status
        return finished, left, right


    @Log.method
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
            if finished:
                break
        else:
            raise Exception("Index not found.")

        return left, right


    @Log.method
    def find(self, direction=False):
        left, right = self.find_edges(direction)
        s = self.degrees_motor_wrapper.scaler

        # determine width of sensor
        if direction:
            if left >= right:
                width = (right + (s*360)) - left
            else:
                width = right - left
        else:
            width = (right - left) if right >= left else ((self.degrees_motor_wrapper.scaler * 360) - left + right)

        distance_to_center = width / 2
        # center of sensor
        center = (left + distance_to_center) % (360 * self.degrees_motor_wrapper.scaler)

        last_position = left if direction else right
        return left, right, center, distance_to_center, last_position

    @Log.method
    def calibrate(self, direction=None):
        left, right, center, distance_to_center, last_position = self.find(direction)
        self.degrees_motor_wrapper._scaled_degrees = self.degrees * self.degrees_motor_wrapper.scaler + (distance_to_center if direction else -distance_to_center)

    @Log.method
    def check_calibration(self, direction=None):
        left, right, center, distance_to_center, last_position = self.find(direction=direction)
        center /= self.degrees_motor_wrapper.scaler
        return abs(center - self.degrees ) < self.tolerance
