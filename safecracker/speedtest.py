from safecracker.defaults import motor


if __name__ == "__main__":
     motor.calibrate_on_index(direction=False)
     motor.degrees_absolute(0, direction=True)

#     motor.calibrate_on_index(direction=True)
#     motor.degrees_absolute(0, direction=True)
