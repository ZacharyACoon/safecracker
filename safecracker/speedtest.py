from safecracker.defaults import motor
import time


if __name__ == "__main__":
     calibration_step_delay = 0.05
     step_delay_start = 100
     step_delay_decrement = 10

     consecutive_failures = 0
     step_delay = step_delay_start
     while True:
         step_delay -= step_delay_decrement
         actual = step_delay / 100000

         motor.raw.default_step_delay = calibration_step_delay
         motor.index.calibrate()
         motor.degrees.absolute(0)
         time.sleep(1)

         motor.raw.default_step_delay = actual
         motor.degrees.absolute(180)
         motor.degrees.absolute(0)

         motor.raw.default_step_delay = calibration_step_delay
         within_tolerance = motor.index.check_calibration()

         if within_tolerance:
             print(f"PASSED: {actual}")
             consecutive_failures = 0
         else:
             print(f"FAILED: {actual}")
             consecutive_failures += 1

         if consecutive_failures > 2:
             print("3 CONSECUTIVE FAILURES.")
             break
