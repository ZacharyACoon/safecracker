import RPi.GPIO as g
from safecracker.defaults import motor


if __name__ == "__main__":
    motor.step_delay = 0.0005
    motor.index.calibrate(direction=False)
    motor.numbers.absolute(0)
