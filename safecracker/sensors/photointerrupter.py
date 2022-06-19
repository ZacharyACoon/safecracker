import RPi.GPIO as g


class Photointerrupter:
    def __init__(self, pin):
        self.pin = pin
        g.setup(self.pin, g.IN)

    def status(self):
        return bool(g.input(self.pin))
