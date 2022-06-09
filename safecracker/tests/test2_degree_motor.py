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
    safecracker.motor.default_step_delay = 0.002
    motor = safecracker.degree_motor_wrapper

    input("Motor should index and goto zero.")
    safecracker.find_index()
    safecracker.zero()

    #input("Motor should turn right, 360 degrees.")
    #list(motor.relative(360))

    #input("Motor should turn left, 360 degrees.")
    #list(motor.relative(-360))

    #input("Motor should turn left 90 degrees.")
    #list(motor.absolute(-90, direction=False))
    #print("position", motor.degrees)

    #input("Motor should turn right 180 degrees.")
    #list(motor.absolute(90, direction=True))
    #print("position", motor.degrees)

    #input("Motor should turn left stopping at each 90 degrees.")
    #for i in range(90, 361, 90):
    #    list(motor.absolute(-i, direction=False))
    #    time.sleep(0.5)

    #input("Motor should tur right stopping at each 90 degrees.")
    #for i in range(90, 361, 90):
    #    list(motor.absolute(i, direction=True))
    #    time.sleep(0.5)

    #for i in range(5, 105, 5):
    #    d = - 360 / 100 * i
    #    list(motor.absolute(d, direction=False))
    #    time.sleep(0.25)

    for i in range(5, 105, 5):
        d = 360 / 100 * i
        list(motor.absolute(d, direction=True))
        input()

    async def async_test():
        input("Motor should turn right, 360 degrees.")
        async for _ in motor.async_relative(360): pass

        input("Motor should turn left, 360 degrees.")
        async for _ in motor.async_relative(-360): pass

#    trio.run(async_test)
