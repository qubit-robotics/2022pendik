import math
import magicbot
import wpilib
from wpimath.controller import PIDController
from subsystems.camera import Camera
from subsystems.drivetrain import DriveTrain
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.climb import Climb
from components.path import RamseteComponent
from components.aimbot import AimBot
import photonvision
import ctre
from wpilib import SmartDashboard as sd

class MyRobot(magicbot.MagicRobot):

    drivetrain: DriveTrain
    shooter: Shooter
    intake: Intake
    camera: Camera
    climb: Climb
    aimbot: AimBot
    # ramsete: RamseteComponent

    def intake_shooter_control(self):
        intake_driverInput = self.flightStick.getRawButton(2)        
        shooter_driverInput = self.flightStick.getRawButton(1)

        if intake_driverInput:
            sd.putString("shooterState","Inactive")
            sd.putBoolean("intakeRunning", True)
            sd.putBoolean("shooterRunning", False)
        if shooter_driverInput:
            sd.putString("IntakeState","Inactive")
            sd.putBoolean("intakeRunning", False)
            sd.putBoolean("shooterRunning", True)

        self.shooter.shooter_begin()
        self.shooter.speed_config()
        self.intake.intake_begin()
    
    def climb_control(self):
        if self.flightStick.getRawButton(6):
            self.climb.move_string(1)
        elif self.flightStick.getRawButton(7):
            self.climb.move_string(-1)
        else:
            self.climb.execute()

    def createObjects(self):
        '''Create motors and stuff here'''
        self.cam = photonvision.PhotonCamera("camera1")
        self.intakespeed = 0.8
        self.drive_fLeft = wpilib.PWMVictorSPX(2)
        self.drive_rLeft = wpilib.PWMVictorSPX(0)
        self.drive_fRight = wpilib.PWMVictorSPX(1)
        self.drive_rRight = wpilib.PWMVictorSPX(3)

        self.drive_fLeft.setSafetyEnabled(0)
        self.drive_rLeft.setSafetyEnabled(0)
        self.drive_fRight.setSafetyEnabled(0)
        self.drive_rRight.setSafetyEnabled(0)

        self.drive_FrontLeftEncoder = wpilib.Encoder(0,1, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.drive_FrontRightEncoder = wpilib.Encoder(5,6, reverseDirection=True, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.drive_FrontLeftEncoder.setDistancePerPulse((15 * math.pi) / 360)
        self.drive_FrontRightEncoder.setDistancePerPulse((15 * math.pi) / 360)

        self.shooter_encoder = wpilib.Encoder(9, 8, encodingType=wpilib.Encoder.EncodingType.k4X, reverseDirection=True)
        self.shooter_encoder.setDistancePerPulse(0.307692308 / 1024) # shooter tekeri eğer düzlemde olsaydı ne kadar yol kat ederdi (bu bize parabol hesaplamasında yardım edecek)

        self.gyro = wpilib.ADIS16448_IMU()
        self.gyro.calibrate()

        self.gamepad = wpilib.Joystick(0)
        self.flightStick = wpilib.Joystick(1)

        self.belt_lower = ctre.WPI_VictorSPX(7)
        self.belt_upper = ctre.WPI_VictorSPX(6)

        self.climb_low = ctre.WPI_VictorSPX(5)
        self.climb_up = ctre.WPI_VictorSPX(4)

        self.switch_upper = wpilib.DigitalInput(3)
        self.switch_lower = wpilib.DigitalInput(4)

        self.shooter_front1 = ctre.WPI_VictorSPX(10)
        self.shooter_front2 = ctre.WPI_VictorSPX(8)
        self.shooter_rear = ctre.WPI_VictorSPX(9)
        self.shooter_front1.setInverted(1)
        self.shooter_rear.setInverted(1)

        self.intake_timer = wpilib.Timer()
        self.shooter_timer = wpilib.Timer()
        self.cooldown_timer = wpilib.Timer() # intake ve shooter komutlarina cooldown ekleyecegiz, karisiklik riski az olacak.

        sd.putNumber("ballCount", 0)
        sd.putBoolean("intakeRunning", False)
        sd.putBoolean("shooterRunning", False)
        sd.putNumber("climbMotor1",0)
        sd.putNumber("climbMotor2",0)
        sd.putBoolean("atis_Kontrol",False)

    def robotPeriodic(self):
        self.camera.get_distance()
        self.camera.get_yaw()
        self.shooter.execute()

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
        
        self.intake_shooter_control()
        self.aimbot.setup()
        self.climb_control()
        self.shooter.speed_config()
        if self.gamepad.getRawButton(5):
            self.aimbot.execute()
        if self.gamepad.getRawButton(6):
            self.drivetrain.enable_slowdown()
            

if __name__ == '__main__':
    wpilib.run(MyRobot)
