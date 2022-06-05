import RPi.GPIO as g


g.setwarnings(False)
g.setmode(g.BOARD)
class Photointerrupter:
    def __init__(self, pin):
        self.pin = pin
        g.setup(self.pin, g.IN)

    def status(self):
        return g.input(self.pin)
