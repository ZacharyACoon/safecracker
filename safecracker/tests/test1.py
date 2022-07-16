from safecracker.defaults import motor
import time


if __name__ == "__main__":
    #motor.step_delay = 0.001
    motor.index.calibrate(direction=False)

    input("test")
    for i in range(10):
        motor.degrees.relative(360)
        motor.degrees.relative(-360)
