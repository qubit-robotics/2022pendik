import magicbot
from components.aimbot import AimBot
from subsystems.intake import Intake
from subsystems.shooter import Shooter
from subsystems.drivetrain import DriveTrain
from wpilib import SmartDashboard as sd

class Deneme(magicbot.AutonomousStateMachine):

    MODE_NAME = "Hub'a yaklas"
    DEFAULT = True

    aimbot: AimBot
    shooter: Shooter
    intake: Intake
    drivetrain: DriveTrain

    _ballsChecked = False
    _shootingBall = False

    _numOfBalls = None

    i = 0

    @magicbot.timed_state(first=True, duration=2, next_state="aim")
    def takeBallsIn(self):
        if (not self._ballsChecked) and self.i != 2:
            sd.putString("IntakeState","Inactive")
            sd.putBoolean("intakeRunning", True)
            sd.putBoolean("shooterRunning", False)
            self.i +=1
            self._ballsChecked = True
        self.intake.intake_begin()
        if self._numOfBalls != sd.getNumber("ballCount", 0):
            self._numOfBalls = sd.getNumber("ballCount", 0)
            self._ballsChecked = False
        self.drivetrain.move(0,-0.5,0)

    @magicbot.state()
    def aim(self):
        state = sd.getBoolean("auto_botInPlace", False)
        if not state:
            self.aimbot.aim(41)
        else:
            self.next_state("shoot")

    @magicbot.state()
    def shoot(self):
        if self._numOfBalls != 0:
            if not self._shootingBall:
                sd.putString("ShooterState","Inactive")
                sd.putBoolean("intakeRunning", False)
                sd.putBoolean("shooterRunning", True)
                self._shootingBall = True
            if sd.getNumber("ballCount", 0) != self._numOfBalls:
                self._numOfBalls = sd.getNumber("ballCount", 0)
                self._shootingBall = False
        else:
            self.done()
        self.shooter.shooter_begin()


