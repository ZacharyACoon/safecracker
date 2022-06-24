from safecracker.defaults import motor
import time


if __name__ == "__main__":
    motor.raw.step_delay = 0.000005
    motor.index.calibrate(direction=False)
    motor.numbers.absolute(0, direction=True)
