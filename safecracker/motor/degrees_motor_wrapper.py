from safecracker.log import Log
import time


class DegreesMotorWrapper(Log):
    def __init__(self, motor, full_step_degrees=1.8, parent_logger=None):
        super().__init__(parent_logger)

        self.motor = motor
        self.scaler = 10 * 1024
        self.full_step_degrees = int(full_step_degrees * self.scaler)
        self._scaled_degrees = 0

    @Log.method(level=3)
    def step(self):
        self.motor.step()
        step_angle = (1 if self.motor.direction else -1) * (self.full_step_degrees // self.motor.microsteps)
        self._scaled_degrees = (self._scaled_degrees + step_angle) % (360 * self.scaler)
        #self.log.debug(f"scaled={self._scaled_degrees}, degrees={self._scaled_degrees // self.scaler}")

    @Log.method
    def steps(self, delta):
        self.motor.direction = delta > 0
        for _ in range(abs(delta)):
            self.step()
            time.sleep(self.motor.default_step_delay / self.motor.microsteps)

    @Log.method
    def relative_to_steps(self, degrees):
        scaled_degrees = int(degrees * self.scaler)
        steps = int((scaled_degrees / self.full_step_degrees) * self.motor.microsteps)
        return steps

    @Log.method
    def relative(self, degrees):
        self.steps(self.relative_to_steps(degrees))

    @Log.method
    def _absolute_to_relative(self, target_degrees, direction=None):
        p = self._scaled_degrees
        t = (target_degrees % 360) * self.scaler
        if t < p:
            left = t - p
            right = (360*self.scaler) - p + t
        else:
            left = -(360*self.scaler) - p + t
            right = t - p

        if direction is False:
            return left
        elif direction is True:
            return right
        elif direction is None:
            if abs(left) < abs(right):
                return left
            else:
                return right

    @Log.method
    def absolute(self, target_degrees, direction=None):
        relative_degrees = (self._absolute_to_relative(target_degrees, direction) // self.scaler)
        self.relative(relative_degrees)

    @property
    def degrees(self):
        return self._scaled_degrees / self.scaler

    @degrees.setter
    def degrees(self, d):
        self._scaled_degrees = int(d * self.scaler)
