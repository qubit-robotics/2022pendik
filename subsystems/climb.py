import wpilib
import ctre
from wpilib import SmartDashboard as sd
import magicbot

class Climb:
    climb_low: ctre.WPI_VictorSPX
    climb_up: ctre.WPI_VictorSPX

    val_string = magicbot.will_reset_to(0)
    val_tilt = magicbot.will_reset_to(0)

    def move_string(self, val):
        self.val_string = val

    def move_tilt(self, val):
        self.val_tilt = val

    def execute(self):
        self.climb_low.set(ctre.ControlMode.PercentOutput, self.val_string)
        self.climb_up.set(ctre.ControlMode.PercentOutput, self.val_tilt)
        