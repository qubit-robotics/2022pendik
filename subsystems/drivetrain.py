import magicbot
import wpilib
import wpilib.drive

class DriveTrain():
    drive_fLeft: wpilib.PWMVictorSPX
    drive_rLeft: wpilib.PWMVictorSPX
    drive_fRight: wpilib.PWMVictorSPX
    drive_rRight: wpilib.PWMVictorSPX

    throttle_y = magicbot.will_reset_to(0) # robotun Y ekseninde ilerlemesi
    throttle_x = magicbot.will_reset_to(0) # robotun X ekseninde ilerlemesi
    rotation = magicbot.will_reset_to(0)

    slowdown = magicbot.will_reset_to(False)

    def setup(self):
        self.drive_fLeft.setInverted(1)
        self.drive_rLeft.setInverted(1)

        self.drive = wpilib.drive.MecanumDrive(
            self.drive_fLeft,
            self.drive_rLeft,
            self.drive_fRight,
            self.drive_rRight,
        )

    def move(self, throttle_x: float, throttle_y: float, rotation: float, slowdown=False):
        self.throttle_y = throttle_y
        self.throttle_x = -throttle_x
        self.rotation = -rotation

        self.slowdown = slowdown
        
    def execute(self):
        if self.slowdown:
            self.drive.driveCartesian(self.throttle_y * 0.5, self.throttle_x * 0.5, self.rotation * 0.5, 0)
        else:
            self.drive.driveCartesian(self.throttle_y, self.throttle_x, self.rotation, 0)

