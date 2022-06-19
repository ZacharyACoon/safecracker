import RPi.GPIO as g
from safecracker.defaults import motor


if __name__ == "__main__":
    print("Please enter the number of steps to travel +right/-left to set the dial to zero.")
    while True:
        raw = input("n, -n, or nothing to finish.\n")
        if raw == "":
            break
        try:
            v = int(raw)
            motor.steps(v)
        except Exception as e:
            print(e)
            print("Entry not recognized.")
    motor.degrees = 0

    index_center = motor.find_index()
    print(f"Assuming you started on exactly 0.  Index's center is located at: {index_center}")
