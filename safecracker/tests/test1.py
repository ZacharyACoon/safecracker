from safecracker.defaults import motor
import time


if __name__ == "__main__":
    motor.step_delay = 0.001
    #motor.numbers.absolute(0, direction=False)
    motor.index.calibrate()
    motor.numbers.absolute(0)

    #input("Should turn right 1 full revolution.")
    #motor.degrees.relative(360)

    #input("Should turn left 1 full revolution.")
    #motor.degrees.relative(-360)

    #input("Should go up 10.")
    #motor.numbers.relative(10)

    #input("Should go down 10.")
    #motor.numbers.relative(-10)

    #motor.raw.step_delay = 0.002
    #motor.index.calibrate(direction=False)
    #motor.numbers.absolute(0, direction=True)
    #print(motor.degrees._scaled_degrees)

