import RPi.GPIO as g
from safecracker.config import get_relative_config_json
from safecracker.safecracker import Safecracker
import trio
import time
import traceback

g.setwarnings(False)
g.setmode(g.BOARD)


if __name__ == "__main__":
    config = get_relative_config_json()
    safecracker = Safecracker(config)
    safecracker.motor.set_microsteps(16)

    print(dir(safecracker))

    print("Please enter the number of steps to travel +right/-left to set the dial to zero.")
    while True:
        raw = input("n, -n, or nothing to finish.\n")
        if raw == "":
            break
        try:
            v = int(raw)
            list(safecracker.degree_motor_wrapper.steps(v))
        except Exception as e:
            print(e)
            print("Entry not recognized.")
    safecracker.degree_motor_wrapper.degrees = 0

    print("Now it should find index automatically.")
    safecracker.indexed_motor_wrapper.find_index()
    print(safecracker.indexed_motor_wrapper.pip)
    print("And zero.")
    safecracker.zero()
