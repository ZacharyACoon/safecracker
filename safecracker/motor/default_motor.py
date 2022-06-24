from safecracker.log import Log


class DefaultMotor(Log):
    def __init__(self, a4988, degrees_motor_wrapper, indexed_motor_wrapper, numbers_motor_wrapper, parent_logger=None):
        super().__init__(parent_logger)
        self.raw = a4988
        self.degrees = degrees_motor_wrapper
        self.index = indexed_motor_wrapper
        self.numbers = numbers_motor_wrapper
