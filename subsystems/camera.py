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
            sd.putNumber("hubDistance", photonvision.PhotonUtils.calculateDistanceToTarget(constants.kCamHeightOffGround,
                                                                    constants.kTargetHeight,
                                                                    radians(constants.kCamPitch),
                                                                    radians(pitch)))
        else:
            sd.delete("hubDistance") #HUD'dan silinmiyor, ama kodun aptal bir sey yapmasindan iyidir.
    
    def get_yaw(self):
        if self.cam.hasTargets():
            sd.putNumber("hubYaw", -self.cam.getLatestResult().getBestTarget().getYaw())
        else:
            sd.delete("hubYaw") #HUD'dan silinmiyor, ama kodun aptal bir sey yapmasindan iyidir.
    
    def execute(self):
        sd.putBoolean("GORUS", self.cam.hasTargets())
