import magicbot
import wpilib
import wpilib.drive

class DriveTrain:
    drive_fLeft: wpilib.PWMVictorSPX
    drive_rLeft: wpilib.PWMVictorSPX
    drive_fRight: wpilib.PWMVictorSPX
    drive_rRight: wpilib.PWMVictorSPX

    throttle_y = 0 # robotun Y ekseninde ilerlemesi
    throttle_x = 0 # robotun X ekseninde ilerlemesi
    rotation = 0

    throttle_left_volts = magicbot.will_reset_to(0)
    throttle_right_volts = magicbot.will_reset_to(0)

    tank_drive = magicbot.will_reset_to(False)

    def setup(self):
        self.drive_fRight.setInverted(1)
        self.drive_rRight.setInverted(1)

        self.drive = wpilib.drive.MecanumDrive(
            self.drive_fLeft,
            self.drive_rLeft,
            self.drive_fRight,
            self.drive_rRight,
        )

    def move(self, throttle_y: float, throttle_x: float, rotation: float):
        self.throttle_y = throttle_y
        self.throttle_x = throttle_x
        self.rotation = rotation

    def tank_move(self, throttle_left_volts, throttle_right_volts):
        self.tank_drive = True

        self.throttle_left_volts = throttle_left_volts
        self.throttle_right_volts = throttle_right_volts

        self.drive_fLeft.setVoltage(self.throttle_left_volts)
        self.drive_rLeft.setVoltage(self.throttle_left_volts)
        self.drive_fRight.setVoltage(self.throttle_right_volts)
        self.drive_rRight.setVoltage(self.throttle_right_volts)
        
    def execute(self):
        if not self.tank_drive:
            self.drive.driveCartesian(-self.throttle_y, self.throttle_x, self.rotation, 0)
        
        else:
            pass

