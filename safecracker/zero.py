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

    safecracker.indexed_motor_wrapper.find_index()
    safecracker.zero()
