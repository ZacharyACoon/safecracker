from safecracker.defaults import motor
import time


if __name__ == "__main__":
    motor.step_delay = 0.001
    motor.index.calibrate(direction=False)

    input("Turn left, stopping every 10.")
    for i in range(0, 110, 10):
        motor.numbers.absolute(i, direction=False)
        time.sleep(0.25)

    input("Turn right, stopping every 10.")
    for i in range(0, -110, -10):
        print(i)
        motor.numbers.absolute(i, direction=True)
        time.sleep(0.25)
