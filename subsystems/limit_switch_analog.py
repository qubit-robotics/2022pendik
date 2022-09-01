import wpilib

class LimitSwitch_AnalogInput:

    def __init__(self, AnalogInput) -> None:
        self.channel = AnalogInput
    
    def get(self):
        if wpilib.AnalogInput(self.channel) > 512:
            return True
        else:
            return False