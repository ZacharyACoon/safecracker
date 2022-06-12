import RPi.GPIO as g
from safecracker.config import get_relative_config_json
from safecracker.safecracker import Safecracker
import time
from pathlib import Path

g.setwarnings(False)
g.setmode(g.BOARD)


if __name__ == "__main__":
    config = get_relative_config_json()
    s = Safecracker(config)
    s.motor.set_microsteps(4)
    s.motor.default_step_delay = 0.003

    print(Path().resolve())
    attempt_log = Path("attempts.log")
    progress_file = Path("progress.txt")

    start = 0
    if progress_file.is_file():
        with open(progress_file) as f:
            start = int(f.read().strip())

    for r, a in s.iterate_through_combinations(start):
        with open(attempt_log, 'a') as f:
            f.write(f"{(r, a)}\n")
        with open(progress_file, 'w') as f:
            f.write(f"{a}")
        if not r:
            print("Something went wrong.")
