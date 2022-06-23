import RPi.GPIO as g
from safecracker.defaults import motor


if __name__ == "__main__":
    motor.raw.default_step_delay = 0.05
    print("Please enter the number to travel to set the dial to zero.")
    print("Floats are supported. ;) 0.1 and so forth.")
    while True:
        raw = input("n, -n, or nothing to finish.\n")
        if raw == "":
            break
        try:
           v = float(raw)
           motor.numbers.relative(v)
           #motor.steps(v)
        except Exception as e:
            print(e)
            print("Entry not recognized.")

    motor.degrees._scaled_degrees = 0
    index_center = motor.index.find(direction=True)[1] / motor.degrees.scaler
    motor.degrees.absolute(0, direction=True)

    print(f"Assuming you started on exactly 0:")
    print(f"    - index's center is located at: {index_center}")
    print(f"    - we should end on 0.")
