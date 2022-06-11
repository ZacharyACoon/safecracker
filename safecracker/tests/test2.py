import RPi.GPIO as g
from safecracker.config import get_relative_config_json
from safecracker.safecracker import Safecracker
import trio
import time

g.setwarnings(False)
g.setmode(g.BOARD)


if __name__ == "__main__":
    config = get_relative_config_json()
    s = Safecracker(config)
    s.motor.set_microsteps(16)
    s.default_step_delay = 0.02

    s.find_index()
    s.zero()

#    input("Right, stopping every 10")
#    for n in range(90, -10, -10):
#        list(s.dial_motor_wrapper.absolute(n, direction=False))
#        time.sleep(0.5)

    input("Left, stopping every 10")
    for n in range(10, 110, 10):
        list(s.dial_motor_wrapper.absolute(n, direction=True))
        time.sleep(0.5)
