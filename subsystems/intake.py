import wpilib
import ctre
from wpilib import SmartDashboard as sd

class Intake:
    belt_upper: ctre.WPI_VictorSPX
    belt_lower: ctre.WPI_VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    intake_timer: wpilib.Timer

    def intake_begin(self):

        if (sd.getBoolean("intakeRunning",False)) and (not (sd.getBoolean("shooterRunning",False))):
            if sd.getNumber("ballCount", 0) == 0:
                return self.intake_firstBall()
            elif sd.getNumber("ballCount", 0) == 1:
                return self.intake_secondBall()
            else:
                sd.putString("IntakeState","2 ADET TOPUN VAR!!!")

    def intake_firstBall(self):
        print('intakefirstball')
        print(self.switch_lower.get())
        if self.switch_upper.get() == True:
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
            sd.putBoolean("intakeRunning", False)
            sd.putString("IntakeState","1. Top yerinde!")
        else:
            self.belt_lower.set(ctre.ControlMode.PercentOutput, -1)
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 0.5)
            sd.putBoolean("intakeRunning", True)
            sd.putString("IntakeState","1. Top yerine geliyor...")
    
    def intake_secondBall(self):
        print('intakesecondball')
        print(self.switch_lower.get())
        if self.switch_lower.get() == False:
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
            self.belt_lower.set(ctre.ControlMode.PercentOutput, -0.6)
            sd.putBoolean("intakeRunning", True)
            sd.putString("IntakeState","2. Top yerine geliyor...")
        elif self.switch_lower.get():
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
            sd.putBoolean("intakeRunning", False)
            sd.putString("IntakeState","2. Top yerinde!")
            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
            self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)

    def execute(self):
        if (not sd.getBoolean("intakeRunning",False)) and (not (sd.getBoolean("shooterRunning",False))):
            if (self.switch_lower.get()) and (self.switch_upper.get()):
                sd.putNumber("ballCount", 2)
            elif (self.switch_lower.get()) and (not self.switch_upper.get()):
                self.belt_lower.set(ctre.ControlMode.PercentOutput, -1)
                self.belt_upper.set(ctre.ControlMode.PercentOutput, 0.5)
            elif (not self.switch_lower.get()) and (self.switch_upper.get()):
                self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
                self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)  
                sd.putNumber("ballCount", 1)
            else:
                sd.putNumber("ballCount",0)

        
