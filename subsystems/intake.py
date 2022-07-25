import wpilib
import ctre
import magicbot
from wpilib import SmartDashboard

class Intake:
    belt_upper: ctre.WPI_VictorSPX
    belt_lower: ctre.WPI_VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    intake_timer: wpilib.Timer

    def intake_begin(self,  shooterRunning, intakeRunning, ballCount):
        if intakeRunning and not shooterRunning:
            if ballCount == 0:
                return self.intake_firstBall(shooterRunning, intakeRunning, ballCount)
            elif ballCount == 1:
                return self.intake_secondBall(shooterRunning, intakeRunning, ballCount)
            else:
                SmartDashboard.putString("IntakeState","2 ADET TOPUN VAR!!!")
                pass
        return shooterRunning, intakeRunning, ballCount

    def intake_firstBall(self, shooterRunning, intakeRunning, ballCount):
        if self.switch_lower.get():
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
            ballCount = 1
            intakeRunning = False
            SmartDashboard.putString("IntakeState","1. Top yerinde!")
            return shooterRunning, intakeRunning, ballCount
        else:
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 1)
            intakeRunning = True
            SmartDashboard.putString("IntakeState","1. Top yerine geliyor...")
            return shooterRunning, intakeRunning, ballCount
    
    def intake_secondBall(self, shooterRunning, intakeRunning, ballCount):
        if self.switch_upper.get():
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 1)
            intakeRunning = True
            SmartDashboard.putString("IntakeState","2. Top yerine geliyor...")
            if self.switch_lower.get():
                self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
                intakeRunning = False
                ballCount = 2
                SmartDashboard.putString("IntakeState","2. Top yerinde!")
                return shooterRunning, intakeRunning, ballCount
            return shooterRunning, intakeRunning, ballCount

        else:
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
            SmartDashboard.putString("IntakeState","Topa yer aciliyor...")
            intakeRunning = True
            return shooterRunning, intakeRunning, ballCount
    
    def execute(self):
        pass




