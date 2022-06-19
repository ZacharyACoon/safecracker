import time


class Degrees:
    def __init__(self, *args, full_step_degrees=1.8, **kwargs):
        super().__init__(*args, **kwargs)
        print("init_degrees")
        self.scaler = 10 * 1024
        self.full_step_degrees = int(full_step_degrees * self.scaler)
        self.degrees = 0

    def step(self):
        super().step()
        step_angle = (1 if self.direction else -1) * (self.full_step_degrees // self.microsteps)
        self.degrees = (self.degrees + step_angle) % (360 * self.scaler)

    def relative_degrees_to_steps(self, degrees):
        degrees = int(degrees * self.scaler)
        steps = int((degrees // self.full_step_degrees) * self.microsteps)
        return steps

    def degrees_relative(self, degrees):
        self.steps(self.relative_degrees_to_steps(degrees))

    def degrees_absolute_to_relative(self, target_degrees, direction=None):
        """
        Determines the number of degrees to move relatively to reach absolute degrees.
        Defaults to the shortest distance or counter clock wise.
        """
        p = self.degrees
        t = target_degrees % (360*self.scaler)
        if t < p:
            left = t - p
            right = (360*self.scaler) - p + t
        else:
            left = -(360*self.scaler) - p + t
            right = t - p

        if direction is False:
            return right
        elif direction is True:
            return left
        elif direction is None:
            if abs(left) < abs(right):
                return left
            else:
                return right

    def degrees_absolute(self, target_degrees, direction=None):
        """
        Rotate to absolute degrees.
        Defaults to the shortest distance.
        """
        relative_degrees = self.degrees_absolute_to_relative(target_degrees, direction)
        print("relative_degrees", relative_degrees // self.scaler)
        self.degrees_relative(relative_degrees // self.scaler)
