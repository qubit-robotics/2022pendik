import math
import magicbot
import wpilib
from wpimath.controller import PIDController
from subsystems.camera import Camera
from subsystems.drivetrain import DriveTrain
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.climb import Climb
from subsystems.limit_switch_analog import LimitSwitch_AnalogInput
from components.path import RamseteComponent
import photonvision
import ctre
from wpilib import SmartDashboard as sd

class MyRobot(magicbot.MagicRobot):

    drivetrain: DriveTrain
    shooter: Shooter
    intake: Intake
    # camera: Camera
    climb: Climb
    # aimbot: AimBot
    # ramsete: RamseteComponent
            
    def climb_control(self):
        self.climbMotor1_LowInput = self.flightStick.getRawButton(4)
        self.climbMotor1_UpInput = self.flightStick.getRawButton(5)
        self.climbMotor2_LowInput = self.flightStick.getRawButton(6)
        self.climbMotor2_UpInput = self.flightStick.getRawButton(7)
        
        # if self.climbMotor1_LowInput:
        #     print("sa")
        #     self.climb_low.set(ctre.ControlMode.PercentOutput, 0)
        # elif self.climbMotor1_UpInput:
        #     sd.putNumber("climbMotor1",1)
        # else:
        #     print("jfkenedy")
        #     self.climb_low.set(ctre.ControlMode.PercentOutput, 1)
        # if self.climbMotor2_LowInput:
        #     sd.putNumber("climbMotor2",-1)
        # elif self.climbMotor2_UpInput:
        #     sd.putNumber("climbMotor2",1)
        # else:
        #     sd.putNumber("climbMotor2",0)

    def intake_shooter_control(self):
        intake_driverInput = self.flightStick.getRawButton(2)        
        shooter_driverInput = self.flightStick.getRawButton(1)
        shooter_changeSpeed_Input = self.flightStick.getRawButtonPressed(3) #Bu diger class'in icinde calismiyor. Neden bilmiyorum.

        if intake_driverInput:
            print("intake tusa basti!")
            sd.putString("shooterState","Inactive")
            sd.putBoolean("intakeRunning", True)
            sd.putBoolean("shooterRunning", False)
        if shooter_driverInput:
            print("shooter tusa basti!")
            sd.putString("IntakeState","Inactive")
            sd.putBoolean("intakeRunning", False)
            sd.putBoolean("shooterRunning", True)

        self.shooter.shooter_begin()
        self.shooter.speed_config(shooter_changeSpeed_Input)
        self.intake.intake_begin()

    def createObjects(self):
        '''Create motors and stuff here'''
        self.cam = photonvision.PhotonCamera("camera1")
        self.intakespeed = 0.8
        self.drive_fLeft = wpilib.PWMVictorSPX(0)
        self.drive_rLeft = wpilib.PWMVictorSPX(1)
        self.drive_fRight = wpilib.PWMVictorSPX(2)
        self.drive_rRight = wpilib.PWMVictorSPX(3)

        self.drive_fLeft.setSafetyEnabled(0)
        self.drive_rLeft.setSafetyEnabled(0)
        self.drive_fRight.setSafetyEnabled(0)
        self.drive_rRight.setSafetyEnabled(0)

        self.drive_FrontLeftEncoder = wpilib.Encoder(0,1, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.drive_FrontRightEncoder = wpilib.Encoder(5,6, reverseDirection=True, encodingType=wpilib.Encoder.EncodingType.k4X)
        self.drive_FrontLeftEncoder.setDistancePerPulse((15 * math.pi) / 1024)
        self.drive_FrontRightEncoder.setDistancePerPulse((15 * math.pi) / 1024)

        self.shooter_encoder = wpilib.Encoder(8, 7, encodingType=wpilib.Encoder.EncodingType.k4X, reverseDirection=True)
        self.shooter_encoder.setDistancePerPulse(0.03 / 1024) # shooter tekeri eğer düzlemde olsaydı ne kadar yol kat ederdi (bu bize parabol hesaplamasında yardım edecek)

        self.gyro = wpilib.ADIS16448_IMU()
        self.gyro.calibrate()

        self.gamepad = wpilib.Joystick(0)
        self.flightStick = wpilib.Joystick(1)

        self.belt_lower = ctre.WPI_VictorSPX(7)
        self.belt_upper = ctre.WPI_VictorSPX(6)

        self.climb_low = ctre.WPI_VictorSPX(4)
        self.climb_up = ctre.WPI_VictorSPX(5)

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

    def atis_kontrol(self):
        pass
        # range = sd.getNumber("hubDistance", 0)
        # tolerance = 0.2
        # if self.shooter_speedChange_value == 0:
        #     goal = 0.5
        # elif self.shooter_speedChange_value == 1:
        #     goal = 1
        # elif self.shooter_speedChange_value == 2:
        #     goal = 3
        # elif self.shooter_speedChange_value == 3:
        #     goal = 2
        # if ((range-tolerance) < goal) and ((range+tolerance) > goal):
        #     sd.putBoolean("atis_Kontrol",True)
        # else:
        #     sd.putBoolean("atis_Kontrol",False)

    # def robotPeriodic(self):
    #     self.camera.get_distance()
    #     self.camera.get_yaw()

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
        # self.climb.set_climbMotorSpeed()
        self.atis_kontrol()
        self.climb_control()
        sd.putNumber("shooter_encoder",self.shooter_encoder.getRate())
        if self.flightStick.getRawButton(4):
            self.shooter.shooter_ramp_up()
        elif not self.flightStick.getRawButton(4):
            self.shooter.shooter_stop()
            

if __name__ == '__main__':
    wpilib.run(MyRobot)
