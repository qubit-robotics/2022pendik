import wpilib
import ctre
import magicbot
from wpilib import SmartDashboard as sd

class ShooterEnabler:
    shooter_front1: ctre.VictorSPX
    shooter_front2: ctre.VictorSPX
    shooter_rear: ctre.VictorSPX
    def shooter_shoot(self):
        front = sd.getNumber("shooter_valueFront", 0.5)
        rear = sd.getNumber("shooter_valueRear", 0.5)
        self.shooter_front1.set(ctre.ControlMode.PercentOutput, -front)
        self.shooter_front2.set(ctre.ControlMode.PercentOutput, front)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, -rear)
    def shooter_stop(self):
        self.shooter_front1.set(ctre.ControlMode.PercentOutput, 0)
        self.shooter_front2.set(ctre.ControlMode.PercentOutput, 0)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, 0)
    def execute(self):
        pass

class Shooter:
    belt_upper: ctre.VictorSPX
    belt_lower: ctre.VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    shooter_front1: ctre.VictorSPX
    shooter_front2: ctre.VictorSPX
    shooter_rear: ctre.VictorSPX

    shooter_timer: wpilib.Timer

    shooter_manual: ShooterEnabler

    ballInPlace = False

    def shooter_begin(self):
        if sd.getBoolean("shooterRunning", False):
            if sd.getNumber("ballCount", 1) >= 1 and not sd.getBoolean("intakeRunning", False):
                if (self.switch_upper.get() == False) and (not self.ballInPlace):
                    sd.putString("shooterState","Top yerinde")
                    self.ballInPlace = True

                if not self.ballInPlace:
                    sd.putString("shooterState","Top yerine geliyor...")
                    self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
                    sd.putBoolean("shooterRunning", True)

                elif self.ballInPlace:
                    sd.putString("shooterState","Top yerinde, atısa baslaniyor...")
                    self.shooter_timer.start()
                    self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
                    if not self.shooter_timer.hasPeriodPassed(3):
                        sd.putString("shooterState","Atisa baslandi!")
                        self.shooter_manual.shooter_shoot()

                    else:
                        sd.putString("shooterState","Atis Bitti.")
                        self.shooter_timer.stop()
                        self.shooter_timer.reset()
                        self.shooter_manual.shooter_stop()
                        sd.putNumber("ballCount", sd.getNumber("ballCount", 1) - 1)
                        sd.putBoolean("shooterRunning", False)
                        self.ballInPlace = False

            else:
                sd.putString("shooterState","Hic Topun Yok!")
                sd.putBoolean("shooterRunning", False)
                

    def execute(self):
        pass
