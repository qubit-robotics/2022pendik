import wpilib

class lm393Encoder(wpilib.Counter):

    holes = 2

    def getRate(self):
        if self.getPeriod() != 0:
            return 1 / self.getPeriod() / self.holes / 2
        else:
            return 0.0