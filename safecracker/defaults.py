from safecracker.motor.a4988 import A4988_Pins, A4988
from safecracker.motor.degrees_motor_wrapper import DegreesMotorWrapper
from safecracker.motor.indexed_motor_wrapper import IndexedMotorWrapper
from safecracker.motor.numbers_motor_wrapper import NumbersMotorWrapper
import RPi.GPIO as g

from safecracker.config import get_relative_config_json
from safecracker.log import Log
from safecracker.log import build_default_root_logger


g.setwarnings(False)
g.setmode(g.BOARD)


class DefaultMotor(Log):
    def __init__(self, a4988, degrees_motor_wrapper, indexed_motor_wrapper, numbers_motor_wrapper, parent_logger=None):
        super().__init__(parent_logger)
        self.raw = a4988
        self.degrees = degrees_motor_wrapper
        self.index = indexed_motor_wrapper
        self.numbers = numbers_motor_wrapper


config = get_relative_config_json()
log = build_default_root_logger()


a4988 = A4988(
    A4988_Pins(**config["hardware"]["a4988_pins"]),
    microsteps=16,
    step_delay=0.01,
    parent_logger=log
)

degrees_motor_wrapper = DegreesMotorWrapper(
    a4988,
    full_step_degrees=config["hardware"]["motor"]["full_step_degrees"],
    parent_logger=log
)

indexed_motor_wrapper = IndexedMotorWrapper(
    degrees_motor_wrapper,
    pin=config["hardware"]["photointerrupter"]["pin"],
    degrees=config["hardware"]["photointerrupter"]["degrees"],
    tolerance=0.1,
    parent_logger=log
)

numbers_motor_wrapper = NumbersMotorWrapper(
    degrees_motor_wrapper,
    config["hardware"]["dial"]["numbers"],
    config["hardware"]["dial"]["tolerance"],
    config["hardware"]["dial"]["left_to_right"],
    parent_logger=log
)

motor = DefaultMotor(
    a4988,
    degrees_motor_wrapper,
    indexed_motor_wrapper,
    numbers_motor_wrapper,
    parent_logger=log
)
