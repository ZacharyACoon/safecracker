from safecracker.motor.default_motor import DefaultMotor
import RPi.GPIO as g


from safecracker.config import get_relative_config_json
from safecracker.log import Log
from safecracker.log import build_default_root_logger
from safecracker.safecracker import Safecracker

g.setwarnings(False)
g.setmode(g.BOARD)


config = get_relative_config_json()
log = build_default_root_logger()


hardware = config["hardware"]


#numbers_motor_wrapper = NumbersMotorWrapper(
#    degrees_motor_wrapper,
#    config["hardware"]["dial"]["numbers"],
#    config["hardware"]["dial"]["tolerance"],
#    config["hardware"]["dial"]["left_to_right"],
#    parent_logger=log
#)

motor = DefaultMotor(
    a4988_pins=hardware["a4988_pins"],
    microsteps_per_step=16,
    full_step_degrees=hardware["motor"]["full_step_degrees"],
    index_pin=hardware["photointerrupter"]["pin"],
    index_degrees=hardware["photointerrupter"]["degrees"],
    index_tolerance_degrees=hardware["photointerrupter"]["tolerance_degrees"],
    numbers=hardware["dial"]["numbers"],
    numbers_tolerance=hardware["dial"]["tolerance"],
    left_to_right=hardware["dial"]["left_to_right"]
)

safecracker = Safecracker(
    motor,
    wheels=config["hardware"]["dial"]["wheels"],
    latch_number=config["hardware"]["dial"]["latch_number"],
    forbidden_range=config["hardware"]["dial"]["last_number_forbidden_range"],
    parent_logger=log
)
