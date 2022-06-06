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

    input("Motor should turn right, 3 steps.")
    for _ in safecracker.motor.steps(3): time.sleep(0.5)

    input("Motor should turn left, 3 steps.")
    for _ in safecracker.motor.steps(-3): time.sleep(0.5)


    async def async_test():
        input("Motor should turn right, 3 steps.")
        async for _ in safecracker.motor.async_steps(3): await trio.sleep(0.5)

        input("Motor should turn left, 3 steps.")
        async for _ in safecracker.motor.async_steps(-3): await trio.sleep(0.5)

    trio.run(async_test)
