import wpilib
import ctre
import magicbot
from wpilib import SmartDashboard as sd
from wpimath.controller import PIDController

class ShooterEnabler:
    shooter_front1: ctre.WPI_VictorSPX
    shooter_front2: ctre.WPI_VictorSPX
    shooter_rear: ctre.WPI_VictorSPX
    shooter_encoder: wpilib.Encoder
    shooter_controller: PIDController

    # Arduino'daki map fonskiyonu bu
    def _map(self, x, in_min, in_max, out_min, out_max):
        return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

    def shooter_shoot(self):
        front = 3
        rear = sd.getNumber("shooter_valueRear", 0.5)

        front_voltage = self.shooter_controller.calculate(abs(self.shooter_encoder.getRate()), front)

        self.shooter_front1.setVoltage(front_voltage)
        self.shooter_front2.setVoltage(front_voltage)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, rear)

        if self.shooter_controller.atSetpoint():
            print("setpointte")
            return True
        else:
            return False

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
    force_shoot= False

    def shooter_begin(self):
        if sd.getBoolean("shooterRunning", False):
            if sd.getNumber("ballCount", 1) >= 1 and not sd.getBoolean("intakeRunning", False):
                if (self.switch_upper.get()) and (not self.ballInPlace):
                    sd.putString("shooterState","Top yerinde")
                    self.ballInPlace = True

                if not self.ballInPlace:
                    sd.putString("shooterState","Top yerine geliyor...")
                    self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
                    sd.putBoolean("shooterRunning", True)

                elif self.ballInPlace:
                    sd.putString("shooterState","Top yerinde, atisa baslaniyor...")
                    self.shooter_timer.start()
                    sd.putString("shooterState","Atisa baslandi!")
                    rpmAdequate = self.shooter_manual.shooter_shoot()
                    if rpmAdequate:
                        print("ust belt calisiyor")
                        self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)

                    elif (not rpmAdequate):
                        print("encoder_hizi = ",rpmAdequate)
                        self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
                        self.force_shoot = True

                    else:
                        sd.putString("shooterState","Atis Bitti.")
                        self.shooter_timer.stop()
                        self.shooter_timer.reset()
                        self.shooter_manual.shooter_stop()
                        self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
                        sd.putNumber("ballCount", sd.getNumber("ballCount", 1) - 1)
                        sd.putBoolean("shooterRunning", False)
                        self.ballInPlace = False
                        self.force_shoot = False

            else:
                sd.putString("shooterState","Hic Topun Yok!")
                sd.putBoolean("shooterRunning", False)
                

    def execute(self):
        pass
