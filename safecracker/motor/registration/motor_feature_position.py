from safecracker.motor.motor_feature_registration_model import Feature


class MotorFeaturePosition:
    def __init__(self):
        self.position = 0
        self.position_count = 200
        self.motor = None

    def register(self, motor):
        self.motor = motor

    def before_set_microsteps(self, microsteps):
        self.position /= self.motor.microsteps
        self.position_count /= self.motor.microsteps
        print("before")

    def after_set_microsteps(self, microsteps):
        self.position *= self.motor.microsteps
        self.position_count *= self.motor.microsteps
        print("after")

    def after_step(self, direction):
        print("AFTER_STEP")
        self.position += 1 if direction else -1
        self.position %= self.position_count
