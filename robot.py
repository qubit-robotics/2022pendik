import magicbot
import wpilib
from subsystems.drivetrain import DriveTrain

class MyRobot(magicbot.MagicRobot):

    drivetrain: DriveTrain

    def createObjects(self):
        '''Create motors and stuff here'''
        self.smart_dashboard = wpilib.SmartDashboard()

        self.drivetrain.drive_fLeft = wpilib.PWMVictorSPX(0)
        self.drivetrain.drive_rLeft = wpilib.PWMVictorSPX(1)
        self.drivetrain.drive_fRight = wpilib.PWMVictorSPX(2)
        self.drivetrain.drive_rRight = wpilib.PWMVictorSPX(3)

        self.gamepad = wpilib.Joystick(0)
        self.flightStick = wpilib.Joystick(1)

    def teleopInit(self):
        '''Called when teleop starts; optional'''

    def teleopPeriodic(self):
        '''Called on each iteration of the control loop'''
        # DRIVETRAIN
        # Gamepad'in kanallari ters, biz normal matematikteki koordinat duzlemini kullanacagiz 
        self.throttle_y_input = self.gamepad.getX()
        self.throttle_x_input = self.gamepad.getY()
        self.rotate_input = self.gamepad.getZ()

        try:
            self.drivetrain.move(self.throttle_y_input, self.throttle_x_input, self.rotate_input)
            self.smart_dashboard.putString("Drivetrain:", "+")

        except:
            self.onException()
            self.smart_dashboard.putString("Drivetrain:", "-")

if __name__ == '__main__':
    wpilib.run(MyRobot)
