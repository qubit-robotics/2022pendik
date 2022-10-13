from math import pi
import wpilib
from custom_sensor_classes.customAbsoluteEncoder import lm393Encoder
import ctre
import magicbot
import constants
from wpilib import SmartDashboard as sd
from wpimath.controller import PIDController, SimpleMotorFeedforwardMeters

class Shooter:
    belt_upper: ctre.WPI_VictorSPX
    belt_lower: ctre.WPI_VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    shooter_front1: ctre.WPI_VictorSPX
    shooter_front2: ctre.WPI_VictorSPX
    shooter_rear: ctre.WPI_VictorSPX

    shooter_front1: ctre.WPI_VictorSPX
    shooter_front2: ctre.WPI_VictorSPX
    shooter_rear: ctre.WPI_VictorSPX

    shooter_encoder_front: lm393Encoder
    shooter_encoder_rear: lm393Encoder

    ballInPlace = False

    flightStick: wpilib.Joystick

    shooterMode = {
        0: "Upper Hub Tarmac Cizgi",
        1: "Lower Hub",
        2: "Upper Hub",
        3: "Upper Hub 2 Metre"
    }

    shooter_speedChange_value = 0
    shooter_speedChanged = False

    front_setpoint = 50
    rear_setpoint = 70

    front_setpoint_mps = 12
    rear_setpoint_mps = 6

    force = False

    def mpsToRotPerSec(self, mps: float, wheel_diameter: float) -> float:
        """
        @param1: The target angular velocity in m/s.
        @param2: The diameter of the wheel in centimeters.
        returns: Target rps for the wheel. 
        """
        return mps / wheel_diameter / pi * 100

    def setup(self):
        self.shooter_controller_front = PIDController(
            0.7,
            0,
            0
        )

        self.shooter_controller_rear = PIDController(
            2,
            0,
            0
        )
        
        self.shooter_controller_front.setTolerance(self.mpsToRotPerSec(1, constants.kDiameterFrontShooterWheel))
        self.shooter_controller_rear.setTolerance(self.mpsToRotPerSec(1, constants.kDiameterRearShooterWheel))

        self.windup_timer = wpilib.Timer()
        self.aftershoot_timer = wpilib.Timer()


    def shooter_begin(self):

        if sd.getBoolean("shooterRunning", False):
            if sd.getNumber("ballCount", 1) >= 1 and not sd.getBoolean("intakeRunning", False):
                if (self.switch_upper.get()) and (not self.ballInPlace):
                    sd.putString("shooterState","Top yerinde")
                    self.belt_upper.set(0)
                    self.ballInPlace = True

                if not self.ballInPlace:
                    sd.putString("shooterState","Top yerine geliyor...")
                    sd.putBoolean("shooterRunning", True)
                    self.belt_upper.setVoltage(6)
                    self.belt_lower.setVoltage(6)

                elif self.ballInPlace:
                    sd.putString("shooterState","Top yerinde, atisa baslaniyor...")
                    sd.putString("shooterState","Atisa baslandi!")
                    self.belt_lower.set(0)
                    self.shooter_ramp_up()

                    if self.switch_upper.get():
                        self.windup_timer.start()
                        if self.windup_timer.get() > 1:
                            self.force = True
                            self.windup_timer.stop()
                            self.windup_timer.reset()
                            self.shooter_controller_front.reset()
                            self.shooter_encoder_front.reset()
                            self.shooter_controller_rear.reset()
                            self.shooter_controller_rear.reset()
                    else:
                        pass
                        self.force = False

                    if (not self.switch_upper.get()):
                        self.aftershoot_timer.start()
                        if self.aftershoot_timer.get() > 1:
                            self.aftershoot_timer.stop()
                            self.aftershoot_timer.reset()
                            self.belt_upper.set(0)
                            self.belt_lower.set(0)
                            sd.putNumber("ballCount", sd.getNumber("ballCount", 1) - 1)
                            sd.putString("shooterState","Atis Bitti.")
                            sd.putBoolean("shooterRunning", False)
                            self.shooter_stop()
                            self.windup_timer.stop()
                            self.windup_timer.reset()
                            self.shooter_encoder_front.reset()
                            self.ballInPlace = False
                            self.force = False

                    elif self.force:
                        self.belt_upper.setVoltage(12)
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
            self.front_setpoint_mps = 12
            self.rear_setpoint_mps = 5
            self.front_setpoint = self.mpsToRotPerSec(
                self.front_setpoint_mps, constants.kDiameterFrontShooterWheel
            )
            self.rear_setpoint = self.mpsToRotPerSec(
                self.rear_setpoint_mps, constants.kDiameterRearShooterWheel
            )

        elif self.shooter_speedChange_value == 1:
            self.front_setpoint_mps = 12
            self.rear_setpoint_mps = 12
            self.front_setpoint = self.mpsToRotPerSec(
                self.front_setpoint_mps, constants.kDiameterFrontShooterWheel
            )
            self.rear_setpoint = self.mpsToRotPerSec(
                self.rear_setpoint_mps, constants.kDiameterRearShooterWheel
            )

        elif self.shooter_speedChange_value == 2:
            self.front_setpoint_mps = 6
            self.rear_setpoint_mps = 6 
            self.front_setpoint = self.mpsToRotPerSec(
                self.front_setpoint_mps, constants.kDiameterFrontShooterWheel
            )
            self.rear_setpoint = self.mpsToRotPerSec(
                self.rear_setpoint_mps, constants.kDiameterRearShooterWheel
            )

        elif self.shooter_speedChange_value == 3:
            self.front_setpoint_mps = 12
            self.rear_setpoint_mps = 6
            self.front_setpoint = self.mpsToRotPerSec(
                self.front_setpoint_mps, constants.kDiameterFrontShooterWheel
            )
            self.rear_setpoint = self.mpsToRotPerSec(
                self.rear_setpoint_mps, constants.kDiameterRearShooterWheel
            )

        if self.shooter_speedChanged:
            self.shooter_speedChanged = False    

            for i in self.shooterMode:
                _state = (i == self.shooter_speedChange_value)
                sd.putBoolean(self.shooterMode.get(i), _state)  

    def shooter_ramp_up(self):
        shooter_pid_val_front = self.shooter_controller_front.calculate(abs(self.shooter_encoder_front.getRate()), self.front_setpoint)
        shooter_pid_val_rear = self.shooter_controller_rear.calculate(self.shooter_encoder_rear.getRate(), self.rear_setpoint)

        shooter_voltage_front = shooter_pid_val_front
        shooter_voltage_rear = shooter_pid_val_rear

        self.shooter_front1.setVoltage(9)
        self.shooter_front2.setVoltage(9)
        self.shooter_rear.setVoltage(shooter_voltage_rear)

    def shooter_stop(self):
        self.shooter_front1.set(0)
        self.shooter_front2.set(0)
        self.shooter_rear.set(0)
    
    def execute(self):
        sd.putNumber("shooter_encoder_front_rps", self.shooter_encoder_front.getRate())
        sd.putNumber("shooter_encoder_rear_rps", self.shooter_encoder_rear.getRate())
        sd.putNumber("front_setpoint in rot", self.front_setpoint)
        sd.putNumber("rear_setpoint in rot", self.rear_setpoint)
        sd.putNumber("front_setpoint in mps", self.front_setpoint_mps)
        sd.putNumber("rear_setpoint in mps", self.rear_setpoint_mps)
