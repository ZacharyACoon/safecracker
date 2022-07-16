import RPi.GPIO as g
from safecracker.defaults import log, config, motor
from safecracker.safecracker import Safecracker


if __name__ == "__main__":
    safecracker = Safecracker(
        motor,
        wheels=config["hardware"]["dial"]["wheels"],
        latch_number=config["hardware"]["dial"]["latch_number"],
        forbidden_range=config["hardware"]["dial"]["last_number_forbidden_range"],
        parent_logger=log
    )
    safecracker.motor.step_delay = 0.002
    safecracker.motor.index.calibrate(direction=False)
    safecracker.enter_combination([8, 71, 78])
