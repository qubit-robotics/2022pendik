import photonvision
from photonvision import PhotonPipelineResult, PhotonTrackedTarget
import constants
from math import radians
from wpilib import SmartDashboard as sd


class Camera:
    cam: photonvision.PhotonCamera

    def get_distance(self):
        if self.cam.hasTargets():
            pitch = self.cam.getLatestResult().getBestTarget().getPitch()
            sd.putNumber(
                "hubDistance",
                photonvision.PhotonUtils.calculateDistanceToTarget(
                    constants.kCamHeightOffGround,
                    constants.kTargetHeight,
                    radians(constants.kCamPitch),
                    radians(pitch),
                )
            )
        else:
            sd.delete(
                "hubDistance"
            )

    def get_yaw(self):
        if self.cam.hasTargets():
            sd.putNumber("hubYaw", -self.cam.getLatestResult().getBestTarget().getYaw())
        else:
            sd.delete(
                "hubYaw"
            )

    def eval_results(self):
        pass
        # range = sd.getNumber("hubDistance", 0)
        # tolerance = 0.2
        # if self.shooter_speedChange_value == 0:
        #     goal = 0.5
        # elif self.shooter_speedChange_value == 1:
        #     goal = 1
        # elif self.shooter_speedChange_value == 2:
        #     goal = 3
        # elif self.shooter_speedChange_value == 3:
        #     goal = 2
        # if ((range-tolerance) < goal) and ((range+tolerance) > goal):
        #     sd.putBoolean("atis_Kontrol",True)
        # else:
        #     sd.putBoolean("atis_Kontrol",False)

    def execute(self):
        sd.putBoolean("GORUS", self.cam.hasTargets())
