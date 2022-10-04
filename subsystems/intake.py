import wpilib
import ctre
from wpilib import SmartDashboard as sd

class Intake:
    belt_upper: ctre.WPI_VictorSPX
    belt_lower: ctre.WPI_VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    intake_timer: wpilib.Timer

    conveyor = False

    def intake_begin(self):

        if (sd.getBoolean("intakeRunning",False)) and (not (sd.getBoolean("shooterRunning",False))):
            if sd.getNumber("ballCount", 0) == 0:
                return self.intake_firstBall()
            elif sd.getNumber("ballCount", 0) == 1:
                return self.intake_secondBall()
            else:
                sd.putString("IntakeState","2 ADET TOPUN VAR!!!")

    def intake_firstBall(self):
        if self.switch_upper.get() == True:
            self.eval()
            self.belt_lower.set(0)
            self.belt_upper.set(0)
            sd.putBoolean("intakeRunning", False)
            sd.putString("IntakeState","1. Top yerinde!")
        else:
            self.belt_lower.setVoltage(12)
            self.belt_upper.setVoltage(6)
            sd.putBoolean("intakeRunning", True)
            sd.putString("IntakeState","1. Top yerine geliyor...")
    
    def intake_secondBall(self):
        if self.switch_upper.get():
            if self.conveyor:
                self.belt_upper.set(0)
                self.belt_lower.set(0)
                self.conveyor = False
            if self.switch_lower.get() == False:
                self.eval()
                self.belt_upper.setVoltage(0)
                self.belt_lower.setVoltage(6)
                sd.putBoolean("intakeRunning", True)
                sd.putString("IntakeState","2. Top yerine geliyor...")
            elif self.switch_lower.get():
                self.eval()
                sd.putBoolean("intakeRunning", False)
                sd.putString("IntakeState","2. Top yerinde!")
                self.belt_lower.set(0)
                self.belt_upper.set(0)
        else:
            self.conveyor = True
            self.belt_lower.setVoltage(8)
            self.belt_upper.setVoltage(4)

    def eval(self):
        if (not (sd.getBoolean("shooterRunning",False))) and (not self.conveyor):
            if (self.switch_lower.get()) and (self.switch_upper.get()):
                sd.putNumber("ballCount", 2)
            elif (self.switch_lower.get()) or (self.switch_upper.get()):
                sd.putNumber("ballCount", 1)
            else:
                sd.putNumber("ballCount",0)
    
    def man_eval(self, decrease, increase):
        if increase and decrease:
            print("iki tusa ayni anda basma!")
        elif increase:
            sd.putNumber("ballCount", sd.getNumber("ballCount", 1) + 1)
        elif decrease:
            sd.putNumber("ballCount", sd.getNumber("ballCount", 1) - 1)
        
    def execute(self):
        pass

        
