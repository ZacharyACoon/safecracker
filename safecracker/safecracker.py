from safecracker.log import Log
from safecracker.motor.index import ToleranceException
from pathlib import Path
import time


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

    #@Log.method
    def index_to_combination(self, v):
        numbers = []
        for i in range(self.wheels-1):
            d, v = divmod(v, self.adjusted_numbers**(self.wheels - i - 1))
            numbers.append(d * self.tolerance)
        numbers.append(v * self.tolerance)
        return numbers

    @Log.method
    def enter_combination_except_last_number(self, combination):
        l = len(combination)
        for i, v in enumerate(combination[:-1]):
            direction = i % 2 != 0
            self.motor.degrees.relative((self.wheels - i) * 360 * (1 if direction else -1))
            self.motor.numbers.absolute(v, direction=direction)
            #self.motor.degrees.absolute(v, direction=direction)
            time.sleep(0.1)

    @Log.method
    def iterate_through_combinations(self, combination_index=0):
        combination_space = self.calculate_combination_space()
        self.log.info(f"We estimate {combination_space} possible combinations.")

        last_validation_time = self.motor.index.last_validation_time
        combination_indexes_since_last_validation = []
        set_start_time = None
        restart = True
        while combination_index < combination_space:
            suspect = False
            combination = self.index_to_combination(combination_index)
            self.log.info(f"combination_index={combination_index}, combination={combination}")
            if combination_index % self.adjusted_numbers == 0 or restart:
                if set_start_time:
                    set_time = time.time() - set_start_time
                    set_count = int(combination_space / self.adjusted_numbers)
                    s = combination_index % self.adjusted_numbers + 1
                    self.log.info(f"Set={s}/{set_count}, SetTime={set_time}, Time={s*set_time}/{set_count*set_time}, MaxETA={(set_count*set_time - s*set_time) / 60 / 60} hours.")

                set_start_time = time.time()
                self.motor.index.calibrate(direction=self.wheels % 2 == 0)
                self.enter_combination_except_last_number(combination)
                self.log.info(f"Rapidly attempting combinations on last wheel.")
                self.motor.degrees.relative(-360)
                restart = False

            combination_indexes_since_last_validation.append((combination_index, combination))

            if combination[-1] in self.forbidden_range:
                self.log.info(f"Skipping combination_index={combination_index}, combination={combination}.  (last number lands in forbidden range={self.forbidden_range})")
                combination_index += 1
                continue

            try:
                self.motor.numbers.absolute(combination[-1], direction=False)
                self.motor.numbers.absolute(self.latch_number, direction=True)
            except ToleranceException:
                suspect = True
                restart = True

            if self.motor.index.last_validation_time != last_validation_time:
                for combination_index, combination in combination_indexes_since_last_validation:
                    self.log.info(f"combination_index={combination_index}, {combination} {'suspect' if suspect else 'not suspect'}.")
                    yield combination_index, combination, suspect
                combination_indexes_since_last_validation = []
                last_validation_time = self.motor.index.last_validation_time
            combination_index += 1

    @Log.method
    def run(self):
        last_combination_index_file = Path("combination_index.txt")
        suspects_file = Path("suspects.txt")

        if last_combination_index_file.is_file():
            with open(last_combination_index_file) as f:
                combination_index = int(f.read().strip())
        else:
            combination_index = 0

        if not suspects_file.is_file():
            with open(suspects_file, "w+") as f:
                f.write(f"combination_index, combination\n")

        for combination_index, combination, suspect in self.iterate_through_combinations(combination_index):
            with open(last_combination_index_file, "w+") as f:
                f.write(f"{combination_index}")

            if suspect:
                with open(suspects_file, "a+") as f:
                    f.write(f"{combination_index}, {combination}\n")

    @Log.method
    def enter_combination(self, combination):
        self.enter_combination_except_last_number(combination)
        self.motor.degrees.relative(-360)
        self.motor.numbers.absolute(combination[-1], direction=False)
        self.motor.numbers.absolute(self.latch_number, direction=True)
        self.motor.numbers.absolute(0, direction=True)
