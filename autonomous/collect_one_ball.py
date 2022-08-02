import magicbot
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.drivetrain import DriveTrain
from wpilib import ADIS16448_IMU
from wpilib import SmartDashboard as sd

class CollectOneBall(magicbot.AutonomousStateMachine):

    drivetrain: DriveTrain
    intake: Intake
    gyro: ADIS16448_IMU

    MODE_NAME = "Onundeki 1 topu al"
    DEFAULT = True

    @magicbot.timed_state(duration=0.1, first=True, must_finish=True, next_state="move")
    def setup_sd(self):
        sd.putBoolean("shooterRunning", False)
        sd.putBoolean("intakeRunning", True)

    @magicbot.timed_state(duration=8, next_state="turn_around")
    def move(self):
        self.drivetrain.move(-0.5, 0, 0)
        self.intake.intake_begin()
    
    @magicbot.timed_state(duration=6)
    def turn_around(self):
        if self.gyro.getGyroAngleY() < 160:
            self.drivetrain.move(0, 0, 0.5)
        else:
            self.drivetrain.stop()