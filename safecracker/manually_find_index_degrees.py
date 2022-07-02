import RPi.GPIO as g
from safecracker.defaults import motor


if __name__ == "__main__":
    motor.driver.step_delay = 0.005
    print("Please enter the number to travel to set the dial to zero.")
    print("Floats are supported. ;) 0.1 and so forth.")
    while True:
        raw = input("n, -n, or nothing to finish.\n")
        if raw == "":
            break
        try:
           v = float(raw)
           motor.numbers.relative(v)
        except Exception as e:
            print(e)
            print("Entry not recognized.")

    motor.position.position = 0
    motor.index.tolerance_degrees = 0
    motor.index.calibrate()
