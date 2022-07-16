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
        self.smart_dashboard = wpilib.SmartDashboard()

        self.drivetrain.drive_fLeft = wpilib.PWMVictorSPX(0)
        self.drivetrain.drive_rLeft = wpilib.PWMVictorSPX(1)
        self.drivetrain.drive_fRight = wpilib.PWMVictorSPX(2)
        self.drivetrain.drive_rRight = wpilib.PWMVictorSPX(3)

        self.gamepad = wpilib.Joystick(0)
        self.flightStick = wpilib.Joystick(1)

        self.belt_lower = ctre.VictorSPX()
        self.belt_upper = ctre.VictorSPX()

        self.shooter_front1 = ctre.VictorSPX()
        self.shooter_front2 = ctre.VictorSPX()
        self.shooter_rear = ctre.VictorSPX()

        self.intake_timer = wpilib.Timer()
        self.shooter_timer = wpilib.Timer()
        self.cooldown_timer = wpilib.Timer() # intake ve shooter komutlarina cooldown ekleyecegiz, karisiklik riski az olacak.

    def teleopInit(self):
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        # DRIVETRAIN
        # Gamepad'in kanallari ters, biz normal matematikteki koordinat duzlemini kullanacagiz 
        self.throttle_y_input = self.gamepad.getX()
        self.throttle_x_input = self.gamepad.getY()
        self.rotate_input = self.gamepad.getZ()

        self.intake_driverInput = self.flightStick.getRawButton(2)
        self.shooter_driverInput = self.flightStick.getRawButton(1)

        try:
            self.drivetrain.move(self.throttle_y_input, self.throttle_x_input, self.rotate_input)
            self.smart_dashboard.putString("Drivetrain:", "+")

        except:
            self.onException()
            self.smart_dashboard.putString("Drivetrain:", "-")
        
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