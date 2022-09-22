from math import fabs
import wpilib
import ctre
import magicbot
from wpilib import SmartDashboard as sd
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters
class Shooter:
    belt_upper: ctre.VictorSPX
    belt_lower: ctre.VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    shooter_front1: ctre.VictorSPX
    shooter_front2: ctre.VictorSPX
    shooter_rear: ctre.VictorSPX

    shooter_timer: wpilib.Timer

    shooter_front1: ctre.WPI_VictorSPX
    shooter_front2: ctre.WPI_VictorSPX
    shooter_rear: ctre.WPI_VictorSPX

    shooter_encoder: wpilib.Encoder

    ballInPlace = False

    flightStick: wpilib.Joystick

    shooterMode = {
        0: "Lower Hub Dipdibe",
        1: "Lower Hub",
        2: "Upper Hub",
        3: "Upper Hub 2 Metre"
    }

    shooter_speedChange_value = 0
    shooter_speedChanged = False

    front_setpoint = 30
    rear_setpoint = 1

    force = False


    def setup(self):
        self.shooter_controller = PIDController(
            0.7,
            0,
            0
        )
        self.shooter_ff = SimpleMotorFeedforwardMeters(
            -1.7686,
            0.17723,
            0.29475
        )

        self.ff_timer = wpilib.Timer()


    def shooter_begin(self):

        if sd.getBoolean("shooterRunning", False):
            if sd.getNumber("ballCount", 1) >= 1 and not sd.getBoolean("intakeRunning", False):
                if (self.switch_upper.get()) and (not self.ballInPlace):
                    sd.putString("shooterState","Top yerinde")
                    self.ballInPlace = True

                if not self.ballInPlace:
                    sd.putString("shooterState","Top yerine geliyor...")
                    sd.putBoolean("shooterRunning", True)

                elif self.ballInPlace:
                    sd.putString("shooterState","Top yerinde, atisa baslaniyor...")
                    sd.putString("shooterState","Atisa baslandi!")
                    self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
                    self.shooter_ramp_up()

                    if self.shooter_controller.atSetpoint():
                        self.ff_timer.start()
                        print("setpointte")
                        if self.ff_timer.get() > 1:
                            self.force = True
                            self.ff_timer.stop()
                            self.ff_timer.reset()
                    else:
                        self.force = False

                    if (not self.switch_upper.get()):
                        sd.putString("shooterState","Atis Bitti.")
                        self.shooter_timer.start()
                        if self.shooter_timer.get() > 2:
                            self.shooter_timer.stop()
                            self.shooter_timer.reset()
                            self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
                            self.belt_lower.set(ctre.ControlMode.PercentOutput, 0)
                            sd.putNumber("ballCount", sd.getNumber("ballCount", 1) - 1)
                            sd.putBoolean("shooterRunning", False)
                            self.shooter_stop()
                            self.shooter_encoder.reset()
                            self.ballInPlace = False
                            self.force = False

                    elif self.force:
                        print("ust belt calisiyor")
                        self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)

            else:
                sd.putString("shooterState","Hic Topun Yok!")
                sd.putBoolean("shooterRunning", False)
                

    def speed_config(self):

        if self.flightStick.getRawButtonPressed(8):
            if self.shooter_speedChange_value < 3:
                self.shooter_speedChange_value += 1
            else:
                self.shooter_speedChange_value = 0
            self.shooter_speedChanged = True

        if self.shooter_speedChange_value == 0:
            self.front_setpoint = 30
            self.rear_setpoint = 0.5            

        elif self.shooter_speedChange_value == 1:
            self.front_setpoint = 60
            self.rear_setpoint = 0.5

        elif self.shooter_speedChange_value == 2:
            self.front_setpoint = 30
            self.rear_setpoint = 1
        
        elif self.shooter_speedChange_value == 3:
            self.front_setpoint = 60
            self.rear_setpoint = 1

        if self.shooter_speedChanged:
            self.shooter_speedChanged = False      

    def shooter_ramp_up(self):
        self.shooter_controller.setTolerance(5)

        shooter_ff_val = self.shooter_ff.calculate(-self.shooter_encoder.getRate(), self.front_setpoint)
        dummyValue = self.shooter_controller.calculate(abs(self.shooter_encoder.getRate()), self.front_setpoint)
        shooter_voltage = shooter_ff_val
        print("setpoint", self.front_setpoint)

        self.shooter_front1.setVoltage(shooter_voltage)
        self.shooter_front2.setVoltage(shooter_voltage)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, self.rear_setpoint)

    def shooter_stop(self):

        self.shooter_front1.set(ctre.ControlMode.PercentOutput, 0)
        self.shooter_front2.set(ctre.ControlMode.PercentOutput, 0)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, 0)
    

    def execute(self):
        sd.putNumber("shooter_encoder",self.shooter_encoder.getRate())
        sd.putNumber("front_setpoint", self.front_setpoint)
        sd.putNumber("rear_setpoint", self.rear_setpoint)
