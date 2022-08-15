import math
import magicbot
import wpilib
from wpimath.controller import PIDController
from subsystems.camera import Camera
from subsystems.drivetrain import DriveTrain
from subsystems.intake import Intake
from subsystems.shooter import Shooter, ShooterEnabler
from subsystems.climb import Climb
from components.path import RamseteComponent
from components.aimbot import AimBot
from components.buttons import ButtonCtrl
import photonvision
import ctre
from wpilib import SmartDashboard as sd

class MyRobot(magicbot.MagicRobot):

    drivetrain: DriveTrain
    shooter: Shooter
    shooter_manual: ShooterEnabler
    intake: Intake
    camera: Camera
    climb: Climb
    aimbot: AimBot
    ramsete: RamseteComponent
    button_ctrl: ButtonCtrl

    def createObjects(self):
        '''Create motors and stuff here'''
        self.cam = photonvision.PhotonCamera("camera1")

        self.drive_fLeft = wpilib.PWMVictorSPX(0)
        self.drive_rLeft = wpilib.PWMVictorSPX(1)
        self.drive_fRight = wpilib.PWMVictorSPX(2)
        self.drive_rRight = wpilib.PWMVictorSPX(3)

        self.drive_fLeft.setSafetyEnabled(0)
        self.drive_rLeft.setSafetyEnabled(0)
        self.drive_fRight.setSafetyEnabled(0)
        self.drive_rRight.setSafetyEnabled(0)

        self.drive_FrontLeftEncoder = wpilib.Encoder(3,4, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.drive_FrontRightEncoder = wpilib.Encoder(5,6, reverseDirection=True, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.drive_FrontLeftEncoder.setDistancePerPulse((15 * math.pi) / 1024)
        self.drive_FrontRightEncoder.setDistancePerPulse((15 * math.pi) / 1024)

        self.shooter_encoder = wpilib.Encoder(7, 8, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.shooter_encoder.setDistancePerPulse(1 / 1024) #Bununla robotu surmedigimiz icin .getRate kac devir dondugunu alsin direk

        self.gyro = wpilib.ADXRS450_Gyro()
        self.gyro.calibrate()

        self.gamepad = wpilib.Joystick(0)
        self.flightStick = wpilib.Joystick(1)

        self.belt_lower = ctre.WPI_VictorSPX(1)
        self.belt_upper = ctre.WPI_VictorSPX(2)

        self.climb_low = ctre.WPI_VictorSPX(4)
        self.climb_up = ctre.WPI_VictorSPX(5)

        self.switch_upper = wpilib.DigitalInput(1)
        self.switch_lower = wpilib.DigitalInput(2)

        self.shooter_front1 = ctre.WPI_VictorSPX(10)
        self.shooter_front2 = ctre.WPI_VictorSPX(8)
        self.shooter_rear = ctre.WPI_VictorSPX(9)

        self.intake_timer = wpilib.Timer()
        self.shooter_timer = wpilib.Timer()
        self.cooldown_timer = wpilib.Timer() # intake ve shooter komutlarina cooldown ekleyecegiz, karisiklik riski az olacak.

        sd.putNumber("ballCount", 1)
        sd.putBoolean("intakeRunning", False)
        sd.putBoolean("shooterRunning", False)
        sd.putNumber("shooter_valueFront", 0.5)
        sd.putNumber("shooter_valueRear", 0.5)
        sd.putNumber("climbMotor1",0)
        sd.putNumber("climbMotor2",0)
        sd.putBoolean("atis_Kontrol",False)

    def robotPeriodic(self):
        self.camera.get_distance()
        self.camera.get_yaw()

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        # DRIVETRAIN
        # Gamepad'in kanallari ters, biz normal matematikteki koordinat duzlemini kullanacagiz 
        self.throttle_y_input = self.gamepad.getRawAxis(0)
        self.throttle_x_input = self.gamepad.getRawAxis(1)
        self.rotate_input = self.gamepad.getRawAxis(2)

        try:
            self.drivetrain.move(self.throttle_y_input, self.throttle_x_input, self.rotate_input)

        except:
            self.onException()
        
        self.button_ctrl.execute()
        self.intake.intake_begin()
        self.shooter.shooter_begin()
        self.climb.execute()

if __name__ == '__main__':
    wpilib.run(MyRobot)
