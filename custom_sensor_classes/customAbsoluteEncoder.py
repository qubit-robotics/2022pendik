import wpilib

class lm393Encoder:

    counter = 0
    rps = 0

    def __init__(self, channel: int, holes: int) -> None:
        self.input = wpilib.DigitalInput(channel)
        self._lastState = self.input.get()
        self.holes = holes
        self.timer = wpilib.Timer()
        self.another_timer = wpilib.Timer()
        self.timer.start()
        self.another_timer.start()
        self._lastTimestamp = self.timer.getFPGATimestamp()

    def periodic(self):
        if (self._lastState != self.input.get()):
            self.counter += 1
            self.pulseLenght = self.timer.getFPGATimestamp() - self._lastTimestamp
            self._lastState = self.input.get()
            self._lastTimestamp = self.timer.getFPGATimestamp()
            self.rps = 1 / self.pulseLenght / (self.holes * 2)
        
    def returnRps(self):
        return self.rps
    
        
