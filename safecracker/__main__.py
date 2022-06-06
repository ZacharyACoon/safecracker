import RPi.GPIO as g
from safecracker.config import get_relative_config_json
from safecracker.safecracker import Safecracker
import trio
import time

g.setwarnings(False)
g.setmode(g.BOARD)


if __name__ == "__main__":
    config = get_relative_config_json()
    safecracker = Safecracker(config)
    safecracker.find_index()
    time.sleep(1)
    list(safecracker.degree_motor_wrapper.absolute(0))
    time.sleep(3)

#    for i in range(0, 359, 90):
#        print(i)
#        list(safecracker.degree_motor_wrapper.absolute(-i, True))
#        time.sleep(0.5)

#    trio.run(app.run_task, "[::]", config["software"]["web"]["port"])
