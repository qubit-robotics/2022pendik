import magicbot
import wpilib
from subsystems.drivetrain import DriveTrain
from subsystems.intake import Intake
from subsystems.shooter import Shooter
import ctre

class MyRobot(magicbot.MagicRobot):

    ballCount = 1 #Robotu icinde 1 top ile baslat
    intakeRunning = False
    shooterRunning = False

    drivetrain: DriveTrain
    intake: Intake
    shooter: Shooter

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

        # self.gyro = wpilib.AnalogGyro(0)

        self.gamepad = wpilib.Joystick(0)
        self.flightStick = wpilib.Joystick(1)

        self.belt_lower = ctre.VictorSPX(7)
        self.belt_upper = ctre.VictorSPX(6)

        self.switch_upper = wpilib.DigitalInput(1)
        self.switch_lower = wpilib.DigitalInput(2)

        self.shooter_front1 = ctre.VictorSPX(10)
        self.shooter_front2 = ctre.VictorSPX(8)
        self.shooter_rear = ctre.VictorSPX(9)

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

        self.intake_driverInput = self.flightStick.getRawButton(2)
        self.shooter_driverInput = self.flightStick.getRawButton(1)

        try:
            self.drivetrain.move(self.throttle_y_input, self.throttle_x_input, self.rotate_input)

        except:
            self.onException()
        
        #INTAKE/SHOOTER
        #ikisi ayni anda calismamasi için bunu yaptim, yoksa sikinti cikabilir
        #TODO: smartdashboard'a ata bu sistemin ne yaptigini?
        if self.intake_driverInput:
            self.intakeRunning = True
            self.shooterRunning = False
        self.intake.intake_begin()
        
        if self.shooter_driverInput:
            self.shooterRunning = True
            self.intakeRunning = False
        self.shooter.shooter_begin(1, 1)
        
        

        

if __name__ == '__main__':
    wpilib.run(MyRobot)