from safecracker.motor.degrees_mixin import Degrees


class Index(Degrees):
    def __init__(self, *args, index_sensor=None, index_degrees=None, index_tolerance_degrees=0.1, **kwargs):
        super(Index, self).__init__(*args, **kwargs)
        print("init_index")
        assert index_sensor
        assert index_degrees
        self.index_sensor = index_sensor
        self.index_degrees = int(index_degrees * self.scaler)
        self.index_tolerance_degrees = int(index_tolerance_degrees * self.scaler)
        self.index_degrees_left = 0
        self.index_degrees_right = 0

    def find_index_edges(self, direction=False):
        self.direction = direction
        while self.index_sensor.status():
            self.step()
        left = None
        right = None
        for i in range(self.relative_degrees_to_steps(360)):
            self.step()
            print(self.index_sensor.status())
            if direction:
                if self.index_sensor.status():
                    if not left:
                        left = self.degrees
                    right = self.degrees
                elif left:
                    break
            else:
                if self.index_sensor.status():
                    if not right:
                        right = self.degrees
                    left = self.degrees
                elif right:
                    break
        else:
            raise Exception("Index not found.")

        return left, right


    def find_index(self, direction=False):
        self.direction = direction
        left, right = self.find_index_edges(direction)

        # determine width of sensor
        if direction:
            width = (left - right) if left >= right else ((self.scaler * 360) - right + left)
        else:
            width = (right - left) if right >= left else ((self.scaler * 360) - left + right)
        distance_to_center = width // 2
        # center of sensor
        center = (left + distance_to_center) % (360 * self.scaler)
        print(f"D={direction}, l={left}, r={right}, w={width}, c={center}")
        return left, center, right, distance_to_center

    def calibrate_on_index(self, direction=False):
        left, center, right, distance_to_center = self.find_index(direction)
        if direction:
            self.degrees = self.index_degrees + distance_to_center + self.full_step_degrees
        else:
            self.degrees = self.index_degrees - distance_to_center - self.full_step_degrees
