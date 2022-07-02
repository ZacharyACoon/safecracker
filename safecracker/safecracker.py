from safecracker.log import Log
from safecracker.motor.a4988 import A4988_Pins, A4988
from safecracker.motor.degrees_motor_wrapper import DegreesMotorWrapper
from safecracker.motor.indexed_motor_wrapper import IndexedMotorWrapper
from safecracker.motor.numbers_motor_wrapper import NumbersMotorWrapper
from mpu6050 import mpu6050
from pathlib import Path


import time
import asyncio


class Safecracker(Log):
    def __init__(self, motor, wheels, latch_number, forbidden_range, parent_logger=None):
        super().__init__(parent_logger)
        self.motor = motor
        self.wheels = wheels
        self.latch_number = latch_number
        self.forbidden_range = range(*forbidden_range)
        self.numbers = self.motor.numbers.numbers
        self.tolerance = self.motor.numbers.tolerance
        self.adjusted_numbers = int(self.numbers / self.tolerance)

    @Log.method
    def calculate_combination_space(self):
        return (self.adjusted_numbers**(self.wheels-1)) * (self.adjusted_numbers - (len(self.forbidden_range) // 2))

    @Log.method
    def index_to_combination(self, v):
        numbers = []
        for i in range(self.wheels-1):
            d, v = divmod(v * self.tolerance, self.numbers**(self.wheels - i - 1))
            numbers.append(d)
        numbers.append(v)
        return numbers

    @Log.method
    def enter_numbers_except_last(self, numbers):
        l = len(numbers)
        for i, v in enumerate(numbers[:-1]):
            direction = i % 2 != 0
            self.motor.degrees.relative((self.wheels - i) * 360 * (1 if direction else -1))
            self.motor.degrees.absolute(v, direction=direction)
            input(f"Should be at {v}")
            time.sleep(0.1)

    @Log.method
    def iterate_through_combinations(self, attempt=0):
        combination_space = self.calculate_combination_space()
        self.log.info(f"We estimate {combination_space} possible combinations.")

        increment = self.motor.numbers.tolerance

        set_start_time = time.time()
        while attempt < combination_space:
            self.motor.index.calibrate(direction=self.wheels % 2 == 0)
            input("Calibrated.")

            cs = self.index_to_combination(attempt)
            self.log.info(f"Entering first digits: {cs[:-1]}")
            self.enter_numbers_except_last(cs)

            self.motor.degrees(-360)
            self.log.info(f"Rapidly attempting last wheel.")
            last_number = cs[-1]
            while last_number < self.numbers:
                if last_number not in self.forbidden_range:
                    self.log.info(f"Attempt={attempt}, Combination={(*cs[:-1], last_number)}")
                    self.motor.numbers.absolute(last_number, direction=False)
                    time.sleep(0.1)
                    input(f"Should be at {last_number}")
                    self.motor.numbers.absolute(self.latch_number, direction=True)
                    time.sleep(0.1)
                    input(f"Should be at {self.latch_number}")

                last_number += self.tolerance
                attempt += 1

            self.log.info("Range finished. Checking calibration.")
            within_tolerance, tolerance = self.motor.index.check_calibration(direction=False)
            set_stop_time = time.time()
            set_time = set_stop_time - set_start_time
            set_count = int(combination_space / self.adjusted_numbers)
            s = attempt % self.adjusted_numbers + 1
            self.log.info(f"Set={s}/{set_count}, SetTime={set_time}, Time={s*set_time}/{set_count*set_time}, MaxETA={(set_count*set_time - s*set_time) / 60 / 60} hours.")
            yield within_tolerance, tolerance, attempt, cs

    @Log.method
    def run(self):
        last_attempt_file = Path("attempt.txt")
        suspects_file = Path("suspects.txt")

        if last_attempt_file.is_file():
            with open(last_attempt_file) as f:
                attempt = int(f.read().strip())
        else:
            attempt = 0

        if not suspects_file.is_file():
            with open(suspects_file, "w") as f:
                f.write(f"within_tolernace, tolerance, attempt, combination\n")

        for within_tolerance, tolerance, attempt, numbers in self.iterate_through_combinations(attempt):
            with open(last_attempt_file, "w") as f:
                f.write(f"{attempt}")

            with open(suspects_file, "a") as f:
                f.write(f"{within_tolerance}, {tolerance}, {attempt}, {numbers}\n")
