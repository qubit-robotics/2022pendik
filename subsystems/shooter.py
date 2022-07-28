import wpilib
import ctre
import magicbot
from wpilib import SmartDashboard

class ShooterEnabler:
    shooter_front1: ctre.VictorSPX
    shooter_front2: ctre.VictorSPX
    shooter_rear: ctre.VictorSPX
    
    def shooter_shoot(self, front, rear):
        """
        """
        self.shooter_front1.set(ctre.ControlMode.PercentOutput, front)
        self.shooter_front2.set(ctre.ControlMode.PercentOutput, front)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, rear)

    def shooter_stop(self):
        """
        """
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

    def shooter_begin(self, shooterRunning, intakeRunning, ballCount, front, rear):
        if shooterRunning:
            if ballCount >= 1 and not intakeRunning:
                if self.switch_upper.get() and not self.ballInPlace:
                    SmartDashboard.putString("shooterState","Top yerinde")
                    self.ballInPlace = True
                    return shooterRunning, intakeRunning, ballCount
                if not self.ballInPlace:
                    SmartDashboard.putString("shooterState","Top yerine geliyor...")
                    self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
                    shooterRunning = True
                    return shooterRunning, intakeRunning, ballCount
                elif self.ballInPlace:
                    SmartDashboard.putString("shooterState","Top yerinde, atısa baslaniyor...")
                    self.shooter_timer.start()
                    self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
                    if not self.shooter_timer.hasPeriodPassed(3):
                        SmartDashboard.putString("shooterState","Atisa baslandi!")
                        self.shooter_manual.shooter_shoot(front, rear)
                        return shooterRunning, intakeRunning, ballCount
                    else:
                        SmartDashboard.putString("shooterState","Atis Bitti.")
                        self.shooter_timer.stop()
                        self.shooter_timer.reset()
                        self.shooter_manual.shooter_stop()
                        ballCount -= 1
                        shooterRunning = False
                        self.ballInPlace = False
                        return shooterRunning, intakeRunning, ballCount
            else:
                SmartDashboard.putString("shooterState","Hic Topun Yok!")
                shooterRunning = False
                return shooterRunning, intakeRunning, ballCount
        else:
            return shooterRunning, intakeRunning, ballCount

    def execute(self):
        pass
