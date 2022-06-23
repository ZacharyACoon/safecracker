from safecracker.defaults import motor
import time


if __name__ == "__main__":
    motor.raw.step_delay = 0.000005

    start = time.time()
    motor.degrees.relative(100 * 360)
    stop = time.time()

    print(f"Elapsed: {stop - start}")
