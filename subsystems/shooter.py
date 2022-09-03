import wpilib
import ctre
import magicbot
from wpilib import SmartDashboard as sd
from wpimath.controller import PIDController
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
    force_shoot= False

    flightStick: wpilib.Joystick

    shooterMode = {0: "Lower Hub Dipdibe",
                    1: "Lower Hub",
                    2: "Upper Hub",
                    3: "Upper Hub 2 Metre"}

    shooter_speedChange_value = 0
    shooter_speedChanged = False

    front_setpoint = 3
    rear_setpoint = 3

    def setup(self):
        self.shooter_controller = PIDController(
            7,
            0,
            0
        )
        self.shooter_controller.setTolerance(0.1)
        sd.putData(self.shooter_controller)


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
                    rpmAdequate = self.shooter_ramp_up()
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
                        self.shooter_stop()
                        self.belt_upper.set(ctre.ControlMode.PercentOutput, 0)
                        sd.putNumber("ballCount", sd.getNumber("ballCount", 1) - 1)
                        sd.putBoolean("shooterRunning", False)
                        self.ballInPlace = False
                        self.force_shoot = False

            else:
                sd.putString("shooterState","Hic Topun Yok!")
                sd.putBoolean("shooterRunning", False)
                

    def speed_config(self, buttonInput):

        if buttonInput:
            if self.shooter_speedChange_value < 3:
                self.shooter_speedChange_value += 1
            else:
                self.shooter_speedChange_value = 0
            self.shooter_speedChanged = True

        if self.shooter_speedChange_value == 0:
            self.front_setpoint = 3
            self.rear_setpoint = 0.5            

        elif self.shooter_speedChange_value == 1:
            self.front_setpoint = 6
            self.rear_setpoint = 0.5

        elif self.shooter_speedChange_value == 2:
            self.front_setpoint = 3
            self.rear_setpoint = 1
        
        elif self.shooter_speedChange_value == 3:
            self.front_setpoint = 6
            self.rear_setpoint = 1

        if self.shooter_speedChanged:
            self.shooter_speedChanged = False

            for i in self.shooterMode:
                _state = (i == self.shooter_speedChange_value)
                sd.putBoolean(self.shooterMode.get(i), _state)


    def shooter_ramp_up(self):

        front_voltage = self.shooter_controller.calculate(abs(self.shooter_encoder.getRate()), self.front_setpoint)

        self.shooter_front1.setVoltage(front_voltage)
        self.shooter_front2.setVoltage(front_voltage)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, self.rear_setpoint)

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
        sd.putNumber("shooter_encoder",self.shooter_encoder.getRate())
