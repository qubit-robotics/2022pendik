import wpilib
import ctre
from wpilib import SmartDashboard as sd

class Climb:
    climb_low: ctre.WPI_VictorSPX
    climb_up: ctre.WPI_VictorSPX

    def execute(self):
        climbMotor1 = sd.getNumber("climbMotor1",0)
        climbMotor2 = sd.getNumber("climbMotor2",0)

        if climbMotor1 == 0:
            self.climb_low.set(ctre.ControlMode.PercentOutput, 0)
        elif climbMotor1 == 1:
            self.climb_low.set(ctre.ControlMode.PercentOutput, 1)
        elif climbMotor1 == -1:
            self.climb_low.set(ctre.ControlMode.PercentOutput, -1)
        if climbMotor2 == 0:
            self.climb_up.set(ctre.ControlMode.PercentOutput, 0)
        elif climbMotor2 == 1:
            self.climb_up.set(ctre.ControlMode.PercentOutput, 1)
        elif climbMotor2 == -1:
            self.climb_up.set(ctre.ControlMode.PercentOutput, -1)
        