import RPi.GPIO as g
from safecracker.config import get_relative_config_json
from safecracker.safecracker import Safecracker
import trio


g.setwarnings(False)
g.setmode(g.BOARD)


def acceleration_profile(i, count):
    return 0.01

    x = i
    #y = -0.0001*(x-1)+0.005

    r = count - i
    if x < 32:
        y = -0.0001*(x-1)+0.005
    elif r < 32:
        y = -0.0001*(r-1)+0.005
    else:
        y = 0.0019

    return y


if __name__ == "__main__":
    config = get_relative_config_json()
    safecracker = Safecracker(config, acceleration_profile)
    safecracker.index()

#    trio.run(app.run_task, "[::]", config["software"]["web"]["port"])
