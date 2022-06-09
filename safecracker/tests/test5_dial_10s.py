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
    motor = safecracker.dial_motor_wrapper

    safecracker.find_index()
    safecracker.zero()
    time.sleep(1)

#    input("Motor should turn left stopping every 10.")
#    for i in range(10, 100, 10):
#        print(i)
#        list(motor.absolute(i, direction=False))
#        time.sleep(0.5)

#    print("Returning to 0")
#    safecracker.zero()

    input("Motor should turn right stopping every 10.")
    for i in range(90, 0, -10):
        print(i)
        list(motor.absolute(i, direction=True))
        time.sleep(0.5)

    async def async_test():
        input("Motor should turn right and stop at index.")
        await motor.async_find_index(direction=True)

        input("Motor should turn left and stop at index.")
        await motor.async_find_index(direction=False)

    #trio.run(async_test)
