import wpilib


class Deneme:
    shooterRunning: bool
    intakeRunning: bool

    gamepad: wpilib.Joystick
    flightStick: wpilib.Joystick

    def execute(self):
        if self.gamepad.getRawButton(1):
            self.shooterRunning = True
        if self.gamepad.getRawButton(2):
            self.shooterRunning = False
        return self.shooterRunning
