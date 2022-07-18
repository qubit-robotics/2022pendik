import wpilib
import ctre
import magicbot

class Intake:
    belt_upper: ctre.VictorSPX
    belt_lower: ctre.VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    ballCount: int

    intakeRunning: bool
    shooterRunning: bool

    intake_timer: wpilib.Timer

    def intake_begin(self):
        if self.ballCount < 2 and not self.shooterRunning:
            if self.ballCount == 0:
                self.intake_firstBall()
            elif self.ballCount == 1:
                self.intake_secondBall()
            else:
                pass
    
    def intake_firstBall(self):
        if self.switch_lower.get():
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
            self.ballCount = 1
            self.intakeRunning = False
        else:
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 1)
            self.intakeRunning = True
    
    def intake_secondBall(self):
        if self.switch_upper.get():
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 1)
            self.intakeRunning = True
            if self.switch_lower.get():
                self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
                self.intakeRunning = False
                self.ballCount = 2

        else:
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
            self.intakeRunning = True
    
    def execute(self):
        self.intake_begin()



