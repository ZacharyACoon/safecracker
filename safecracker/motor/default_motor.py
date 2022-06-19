from safecracker.motor.a4988 import A4988
from safecracker.motor.degrees_mixin import Degrees
from safecracker.motor.index_mixin import Index

class DefaultMotor(Index, A4988):
    pass
