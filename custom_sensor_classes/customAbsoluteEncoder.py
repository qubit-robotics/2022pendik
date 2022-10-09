import wpilib

class lm393Encoder:

    counter = 0
    rps = 0
    gearRatio = 1.0

    def __init__(self, channel: int, holes: int) -> None:
        self.input = wpilib.DigitalInput(channel)
        self._lastState = self.input.get()
        self.holes = holes
        self.timer = wpilib.Timer()
        self.another_timer = wpilib.Timer()
        self.timer.start()
        self._lastTimestamp = self.timer.getFPGATimestamp()
    
    def setGearRatio(self, ratio = 1.0):
        """
        @param1: The ratio between the encoder and the output shaft. Should be (input shaft teeth / output shaft teeth). Defaults to 1:1.
        """
        self.gearRatio = ratio

    def reset(self):
        self.counter = 0
        self.rps = 0
        self._lastState = self.input.get()

    def periodic(self):
        if (self._lastState != self.input.get()):
            self.counter += 1
            self.pulseLenght = self.timer.getFPGATimestamp() - self._lastTimestamp
            self._lastState = self.input.get()
            self._lastTimestamp = self.timer.getFPGATimestamp()
            self.rps = 1 / self.pulseLenght / (self.holes * 2) * self.gearRatio
        
    def returnRps(self):
        return self.rps
    
        
