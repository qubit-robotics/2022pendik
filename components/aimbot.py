import wpilib
import photonvision
from wpimath.controller import PIDController
from wpilib import SmartDashboard as sd
from subsystems.drivetrain import DriveTrain

class AimBot:

    LINEAR_P = 8
    LINEAR_D = 0.2
    ANGULAR_P = 0.01
    ANGULAR_D = 0

    cam: photonvision.PhotonCamera
    drivetrain: DriveTrain

    def setup(self):

        self.desiredDistance = 3
        self.turnController = PIDController(self.ANGULAR_P, 0, self.ANGULAR_D)
        self.forwardController = PIDController(self.LINEAR_P, 0, self.LINEAR_D)
    
    def aim(self, desiredDistance):

        self.desiredDistance = desiredDistance

        if self.cam.hasTargets():
            rotationSpeed = self.turnController.calculate(sd.getNumber("hubYaw", 0), 0)
            forwardSpeed = self.forwardController.calculate(sd.getNumber("hubDistance", 0), self.desiredDistance)

            self.turnController.setTolerance(10)
            self.forwardController.setTolerance(0.1)
            sd.putBoolean("auto_turnControllerSetpoint", self.turnController.atSetpoint())
            sd.putBoolean("auto_forwardControllerSetpoint", self.forwardController.atSetpoint())

            if not self.turnController.atSetpoint():
                self.drivetrain.move(0, 0, rotationSpeed)

            elif not self.forwardController.atSetpoint():
                self.drivetrain.move(0, forwardSpeed, 0)
            
            if self.turnController.atSetpoint() and self.forwardController.atSetpoint():
                sd.putBoolean("auto_botInPlace", True)
            
            else:
                sd.putBoolean("auto_botInPlace", False)

        else:
            self.drivetrain.move(0,0,0.2)

    def execute(self):
        pass