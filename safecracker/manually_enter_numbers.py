import RPi.GPIO as g
from safecracker.defaults import safecracker as s


if __name__ == "__main__":
    s.motor.driver.step_delay = 0.005
    s.motor.index.calibrate(direction=False)

    print("Please enter the number to travel.  -+360.0")
    while True:
        raw = input("n, -n, or nothing to finish.\n")
        if raw == "":
            break
        try:
           v = float(raw)
           s.motor.numbers.relative(v)
        except Exception as e:
            print(e)
            print("Entry not recognized.")
