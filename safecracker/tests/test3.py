import RPi.GPIO as g
from safecracker.defaults import log, config, motor
from safecracker.safecracker import Safecracker
import time
from pathlib import Path

g.setwarnings(False)
g.setmode(g.BOARD)


if __name__ == "__main__":
    s = Safecracker(
        motor,
        wheels=config["hardware"]["dial"]["wheels"],
        latch_number=config["hardware"]["dial"]["latch_number"],
        forbidden_range=config["hardware"]["dial"]["last_number_forbidden_range"],
        parent_logger=log
    )

    for i in range(26200, 26300):
        c = s.index_to_combination(i)
        print(i, c)
