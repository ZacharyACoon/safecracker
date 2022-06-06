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
    motor = safecracker.degree_motor_wrapper

#    input("Motor should turn right, 360 degrees.")
#    list(motor.relative(360))

#    input("Motor should turn left, 360 degrees.")
#    list(motor.relative(-360))

    input("Motor should turn left 90 degrees.")
    list(motor.absolute(-90, direction=False))
    print("position", motor.degrees)

    input("Motor should turn right 180 degrees.")
    list(motor.absolute(90, direction=True))
    print("position", motor.degrees)


    async def async_test():
        input("Motor should turn right, 360 degrees.")
        async for _ in motor.async_relative(360): pass

        input("Motor should turn left, 360 degrees.")
        async for _ in motor.async_relative(-360): pass

#    trio.run(async_test)
