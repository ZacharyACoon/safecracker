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

#    input("Should turn right and stop at each 90 degrees.  75, 50, 25, 0")
#    for d in range(90, 450, 90):
#        list(s.degree_motor_wrapper.absolute(d, direction=False))
#        time.sleep(1)

    input("Should turn left and stop at each 90 degrees. 25, 50, 75, 0")
    for d in range(-90, -450, -90):
        print(d, d%360)
        list(s.degree_motor_wrapper.absolute(d, direction=True))
        time.sleep(1)
        input()
