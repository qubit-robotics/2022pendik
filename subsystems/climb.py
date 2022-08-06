import wpilib
import ctre
from wpilib import SmartDashboard as sd

class Climb:
    climb_low: ctre.WPI_VictorSPX
    climb_up: ctre.WPI_VictorSPX

    def set_climbMotorSpeed(self):
        if sd.getNumber("climbMotor1",0):
            self.climb_low(ctre.ControlMode.PercentOutput, 0)
        elif sd.getNumber("climbMotor1",1):
            self.climb_low(ctre.ControlMode.PercentOutput, 1)
        elif sd.getNumber("climbMotor1",-1):
            self.climb_low(ctre.ControlMode.PercentOutput, -1)
        if sd.getNumber("climbMotor2",0):
            self.climb_up(ctre.ControlMode.PercentOutput, 0)
        elif sd.getNumber("climbMotor2",1):
            self.climb_up(ctre.ControlMode.PercentOutput, 1)
        elif sd.getNumber("climMotor2",-1):
            self.climb_up(ctre.ControlMode.PercentOutput, -1)
        