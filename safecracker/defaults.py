import RPi.GPIO as g
from safecracker.config import get_relative_config_json
from safecracker.motor.a4988 import A4988_Pins
from safecracker.motor.default_motor import DefaultMotor
from safecracker.sensors.photointerrupter import Photointerrupter


g.setwarnings(False)
g.setmode(g.BOARD)


config = get_relative_config_json()
motor = DefaultMotor(
    A4988_Pins(**config["hardware"]["a4988_pins"]),
    microsteps=16,
    default_step_delay=0.005,
    full_step_degrees=config["hardware"]["motor"]["full_step_degrees"],
    index_sensor=Photointerrupter(config["hardware"]["photointerrupter"]["pin"]),
    index_degrees=config["hardware"]["photointerrupter"]["degrees"],
    index_tolerance_degrees=0.1
)
