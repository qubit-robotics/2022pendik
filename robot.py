from re import S
import magicbot
import wpilib
from subsystems.drivetrain import DriveTrain
from subsystems.intake import Intake
from subsystems.shooter import Shooter, ShooterEnabler
import ctre
from wpilib import SmartDashboard

class MyRobot(magicbot.MagicRobot):

    ballCount = 1 #Robotu icinde 1 top ile baslat

    shooter_speedChange_value = 0
    shooter_speedChanged = False

    shooterRunning = False
    intakeRunning = False

    shooter_valueFront = 0.5
    shooter_valueRear = 0.5

    shooterMode = {0: "Lower Hub Dipdibe",
                   1: "Lower Hub",
                   2: "Upper Hub",
                   3: "Upper Hub 2 Metre"}

    drivetrain: DriveTrain
    shooter: Shooter
    shooter_manual: ShooterEnabler
    intake: Intake

    def shooter_speed_configuration(self):

        if self.shooter_speedChange_value == 0:
            self.shooter_valueFront = 0.5
            self.shooter_valueRear = 0.5
            

        if self.shooter_speedChange_value == 1:
            self.shooter_valueFront = 1
            self.shooter_valueRear = 0.5
        
        if self.shooter_speedChange_value == 2:
            self.shooter_valueFront = 0.5
            self.shooter_valueRear = 1
        
        if self.shooter_speedChange_value == 3:
            self.shooter_valueFront = 1
            self.shooter_valueRear = 1

        if self.shooter_speedChanged:
            self.shooter_speedChanged = False

            for i in self.shooterMode:
                _state = (i == self.shooter_speedChange_value)
                SmartDashboard.putBoolean(self.shooterMode.get(i), _state)
            

    def intake_shooter_control(self):
        self.intake_driverInput = self.flightStick.getRawButton(2)
        self.shooter_driverInput = self.flightStick.getRawButton(1)
        self.shooter_changeSpeed_Input = self.flightStick.getRawButtonPressed(3)

        if self.intake_driverInput:
            print("intake tusa basti!")
            SmartDashboard.putString("shooterState","Inactive")
            self.intakeRunning = True
            self.shooterRunning = False

        
        if self.shooter_driverInput:
            print("shooter tusa basti!")
            SmartDashboard.putString("IntakeState","Inactive")
            self.shooterRunning = True
            self.intakeRunning = False
        
        if self.shooter_changeSpeed_Input:
            if self.shooter_speedChange_value < 3:
                self.shooter_speedChange_value += 1
            else:
                self.shooter_speedChange_value = 0
            self.shooter_speedChanged = True

        self.shooterRunning, self.intakeRunning, self.ballCount = self.shooter.shooter_begin(self.shooterRunning,
                                                                                             self.intakeRunning,
                                                                                             self.ballCount,
                                                                                             self.shooter_valueFront,
                                                                                             self.shooter_valueRear)
        
        self.shooterRunning, self.intakeRunning, self.ballCount = self.intake.intake_begin(self.shooterRunning, 
                                                                                           self.intakeRunning, 
                                                                                           self.ballCount)

    def createObjects(self):
        '''Create motors and stuff here'''

        self.drive_fLeft = wpilib.PWMVictorSPX(0)
        self.drive_rLeft = wpilib.PWMVictorSPX(1)
        self.drive_fRight = wpilib.PWMVictorSPX(2)
        self.drive_rRight = wpilib.PWMVictorSPX(3)

        self.drive_fLeft.setSafetyEnabled(0)
        self.drive_rLeft.setSafetyEnabled(0)
        self.drive_fRight.setSafetyEnabled(0)
        self.drive_rRight.setSafetyEnabled(0)

        self.gyro = wpilib.AnalogGyro(0)

        self.gamepad = wpilib.Joystick(0)
        self.flightStick = wpilib.Joystick(1)

        self.belt_lower = ctre.WPI_VictorSPX(1)
        self.belt_upper = ctre.WPI_VictorSPX(2)

        self.switch_upper = wpilib.DigitalInput(1)
        self.switch_lower = wpilib.DigitalInput(2)

        self.shooter_front1 = ctre.WPI_VictorSPX(10)
        self.shooter_front2 = ctre.WPI_VictorSPX(8)
        self.shooter_rear = ctre.WPI_VictorSPX(9)

        self.intake_timer = wpilib.Timer()
        self.shooter_timer = wpilib.Timer()
        self.cooldown_timer = wpilib.Timer() # intake ve shooter komutlarina cooldown ekleyecegiz, karisiklik riski az olacak.

    def teleopInit(self):
        '''Called when teleop starts; optional'''

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
        self.shooter_speed_configuration()

        wpilib.SmartDashboard.putNumber("ballCount", self.ballCount)
        wpilib.SmartDashboard.putBoolean("intakeRunning", self.intakeRunning)
        wpilib.SmartDashboard.putBoolean("shooterRunning", self.shooterRunning)
        
    
        
        

        

if __name__ == '__main__':
    wpilib.run(MyRobot)