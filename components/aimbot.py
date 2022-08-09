import wpilib
import photonvision
from wpimath.controller import PIDController
from wpilib import SmartDashboard as sd
from subsystems.drivetrain import DriveTrain

class AimBot:

    LINEAR_P = 0.5
    LINEAR_D = 0.2
    ANGULAR_P = 0.01
    ANGULAR_D = 0.005

    cam: photonvision.PhotonCamera
    drivetrain: DriveTrain

    def setup(self):

        self.desiredDistance = 3
        self.turnController = PIDController(self.ANGULAR_P, 0, self.ANGULAR_D)
        self.forwardController = PIDController(self.LINEAR_P, 0, self.LINEAR_D)
    
    def aim(self, desiredDistance):

        self.desiredDistance = desiredDistance

    def execute(self):

        if self.cam.hasTargets():
            print("here")
            rotationSpeed = self.turnController.calculate(sd.getNumber("hubYaw", 0), 0)
            forwardSpeed = self.forwardController.calculate(sd.getNumber("hubDistance", 0), self.desiredDistance)

            self.turnController.setTolerance(5)
            self.forwardController.setTolerance(0.1)

            if self.turnController.atSetpoint() and self.forwardController.atSetpoint():
                sd.putBoolean("auto_botInPlace", True)
            else:
                print("gitti", forwardSpeed, rotationSpeed)
                self.drivetrain.move(forwardSpeed, 0.0, rotationSpeed)
                sd.putBoolean("auto_botInPlace", False)
        else:
            self.drivetrain.move(0,0,0.5)