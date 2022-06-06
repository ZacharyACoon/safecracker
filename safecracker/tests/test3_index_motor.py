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
    safecracker.motor.default_step_delay = 0.02
    motor = safecracker.indexed_motor_wrapper


    input("Motor should turn right and stop at index.")
    motor.find_index(direction=True)


    input("Motor should turn left and stop at index.")
    motor.find_index(direction=False)


    async def async_test():
        input("Motor should turn right and stop at index.")
        await motor.async_find_index(direction=True)

        input("Motor should turn left and stop at index.")
        await motor.async_find_index(direction=False)

    trio.run(async_test)
