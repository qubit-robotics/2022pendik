#
# See the notes for the other physics sample
#

import wpilib.simulation
import wpilib

import halsim_gui
import hal

import ctre
import ctre._simvictorspx

import constants

import wpimath.geometry

from pyfrc.physics.core import PhysicsInterface
import pyfrc.physics.drivetrains
from pyfrc.physics.units import units

from wpimath.system.plant import DCMotor

from photonvision import SimPhotonCamera, SimVisionTarget, SimVisionSystem

import typing

if typing.TYPE_CHECKING:
    from robot import MyRobot

EDGE = 8
INDEXER_LEN = 12
SENSOR_Y = 15

GRAY = wpilib.Color8Bit(wpilib.Color.kGray)

class PhysicsEngine:
    """
    Simulates a 4-wheel mecanum robot using Tank Drive joystick control
    """


    def __init__(self, physics_controller: PhysicsInterface, robot: "MyRobot"):
        """
        :param physics_controller: `pyfrc.physics.core.Physics` object
                                   to communicate simulation effects to
        """
        self.field = wpilib.Field2d()

        self.physics_controller = physics_controller

        # Motors
        self.lf_motor = wpilib.simulation.PWMSim(robot.drive_fLeft.getChannel())
        self.lr_motor = wpilib.simulation.PWMSim(robot.drive_rLeft.getChannel())
        self.rf_motor = wpilib.simulation.PWMSim(robot.drive_fRight.getChannel())
        self.rr_motor = wpilib.simulation.PWMSim(robot.drive_rRight.getChannel())

        self.FrontLeft_encoder = wpilib.simulation.EncoderSim(robot.drive_FrontLeftEncoder)
        self.FrontRight_encoder = wpilib.simulation.EncoderSim(robot.drive_FrontRightEncoder)

        self.left_encoder_counter_front = 0.0
        self.right_encoder_counter_front = 0.0

        # Gyro
        self.gyro = wpilib.simulation.ADXRS450_GyroSim(robot.gyro)

        self.belt_upper_collection = robot.belt_upper.getSimCollection()
        self.belt_lower_collection = robot.belt_lower.getSimCollection()

        self.belt_upper_gui = hal.SimDevice("Upper Belt[1]")
        self.belt_lower_gui = hal.SimDevice("Lower Belt[1]")

        self.belt_upper_sim = wpilib.simulation.DCMotorSim(DCMotor.CIM(), 0.25, 0.00005)
        self.belt_lower_sim = wpilib.simulation.DCMotorSim(DCMotor.CIM(), 0.25, 0.00005)
        
        self.belt_upper_sim_output = self.belt_upper_gui.createDouble("Output", False, 0)
        self.belt_lower_sim_output = self.belt_lower_gui.createDouble("Output", False, 0)

        self.drivetrain = pyfrc.physics.drivetrains.MecanumDrivetrain(
            0.5 * units.meter,
            0.5 * units.meter,
            1 * units.mps
        )


        ##Photonvision
        self.cam = SimVisionSystem("camera1",
                                    constants.kCamDiagFOV,
                                    constants.kCamPitch,
                                    wpimath.geometry.Transform2d(), #Kameranin robotun merkezinde ve 76cm yuksekte kabul ediyorum.
                                    constants.kCamHeightOffGround,
                                    constants.kMaxLEDRange,
                                    constants.kCamResolutionWidth,
                                    constants.kCamResolutionHeight,
                                    10)

        #Sahanin ortasinda 1 adet her tarafa bakan reflektif bant oldugunu varsayiyorum.
        self.targetPose = wpimath.geometry.Pose2d(wpimath.geometry.Translation2d(x=8.23, y=4.115), wpimath.geometry.Rotation2d(0.0))
        self.cam.addSimVisionTarget(SimVisionTarget(self.targetPose, 2.64, 0.14, 0.05))
        
    def update_sim(self, now: float, tm_diff: float) -> None:
        """
        Called when the simulation parameters for the program need to be
        updated.

        :param now: The current time as a float
        :param tm_diff: The amount of time that has passed since the last
                        time that this function was called
        """

        # Simulate the drivetrain
        lf_motor = self.lf_motor.getSpeed()
        lr_motor = self.lr_motor.getSpeed()
        rf_motor = self.rf_motor.getSpeed()
        rr_motor = self.rr_motor.getSpeed()

        speeds = self.drivetrain.calculate(lf_motor, lr_motor, rf_motor, rr_motor)
        pose = self.physics_controller.drive(speeds, tm_diff)

        v = wpilib.simulation.RoboRioSim.getVInVoltage()

        self.belt_upper_collection.setBusVoltage(v)
        self.belt_lower_collection.setBusVoltage(v)

        self.belt_upper_sim.setInputVoltage(self.belt_upper_collection.getMotorOutputLeadVoltage())
        self.belt_lower_sim.setInputVoltage(self.belt_lower_collection.getMotorOutputLeadVoltage())

        self.belt_upper_sim.update(tm_diff)
        self.belt_lower_sim.update(tm_diff)

        self.belt_upper_sim_output.set(self.belt_upper_collection.getMotorOutputLeadVoltage())
        self.belt_lower_sim_output.set(self.belt_lower_collection.getMotorOutputLeadVoltage())

        #PhotonVision



        # wpilib.SmartDashboard.putNumber("belt_upper_sim_val", self.belt_upper_sim.getOutput())
        # wpilib.SmartDashboard.putNumber("belt_lower_sim_val", self.belt_lower_sim.getOutput())


        # Update the gyro simulation
        # -> FRC gyros are positive clockwise, but the returned pose is positive
        #    counter-clockwise
        self.gyro.setAngle(-pose.rotation().degrees())

        self.model = wpilib.Mechanism2d(30, 30)
        wpilib.SmartDashboard.putData("Model", self.model)

        self.field.setRobotPose(pose)
        self.cam.processFrame(pose)

        self.left_encoder_counter_front += self.drivetrain.wheelSpeeds.frontLeft * tm_diff
        self.right_encoder_counter_front += self.drivetrain.wheelSpeeds.frontRight * tm_diff

        self.FrontLeft_encoder.setDistance(self.left_encoder_counter_front)
        self.FrontRight_encoder.setDistance(self.right_encoder_counter_front)

        self.FrontLeft_encoder.setRate(self.drivetrain.wheelSpeeds.frontLeft)
        self.FrontRight_encoder.setRate(self.drivetrain.wheelSpeeds.frontRight)

