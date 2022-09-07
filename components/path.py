import wpilib


import wpimath.controller
import wpimath.kinematics
import wpimath.trajectory
import wpimath.trajectory.constraint
from wpimath.geometry import Rotation2d, Translation2d


import constants
from subsystems.drivetrain import DriveTrain


class TState:
    done = False


class RamseteComponent:

    drivetrain: DriveTrain
    gyro: wpilib.ADIS16448_IMU
    drive_FrontLeftEncoder : wpilib.Encoder
    drive_FrontRightEncoder: wpilib.Encoder

    kP = 0.5
    kI = 0
    kD = 0

    # Baseline values for a RAMSETE follower in units of meters
    # and seconds. These are recommended, but may be changes if wished.
    kRamseteB = 2
    kRamseteZeta = 0.7

    def setup(self) -> None:
        self._state = None

        self._timer = wpilib.Timer()

        print("setup", )

        self._kinematics = wpimath.kinematics.MecanumDriveKinematics(
            Translation2d(x=0.25, y=0.25),
            Translation2d(x=0.25, y=-0.25),
            Translation2d(x=-0.25, y=0.25),
            Translation2d(x=-0.25, y=-0.25)
        )

        self._odometry = wpimath.kinematics.MecanumDriveOdometry(
            self._kinematics,
            Rotation2d.fromDegrees(-self.gyro.getAngle())
        )

        self._controller = wpimath.controller.RamseteController(
            self.kRamseteB, self.kRamseteZeta
        )

        self._ff = wpimath.controller.SimpleMotorFeedforwardMeters(
            constants.kS_linear, constants.kV_linear, constants.kA_linear
        )

        constraint = wpimath.trajectory.constraint.MecanumDriveKinematicsConstraint(
            self._kinematics, 1
        )

        self.tconfig = wpimath.trajectory.TrajectoryConfig(
            1,
            constants.kMaxAccelerationMetersPerSecondSquared,
        )

        self.tconfig.setKinematics(self._kinematics)
        self.tconfig.addConstraint(constraint)

        self.frontLeft_controller = wpimath.controller.PIDController(self.kP, self.kI, self.kD)
        self.frontRight_controller = wpimath.controller.PIDController(self.kP, self.kI, self.kD)

    def on_disable(self):
        self._state = None

    def startTrajectory(self, trajectory: wpimath.trajectory.Trajectory) -> TState:

        if self._state:
            self._state.done = True

        self._state = TState()
        self._trajectory = trajectory

        initialState = self._trajectory.sample(0)
        self._prevSpeeds = self._kinematics.toWheelSpeeds(
            wpimath.kinematics.ChassisSpeeds(
                initialState.velocity, 0, initialState.velocity * initialState.curvature
            )
        )

        # TODO: probably shouldn't do this here.. oh well
        self._odometry.resetPosition(
            trajectory.initialPose(), Rotation2d.fromDegrees(-self.gyro.getAngle()))

        self.drive_FrontLeftEncoder.reset()
        self.drive_FrontRightEncoder.reset()

        self._timer.reset()
        self._timer.start()
        self._lastTm = -1

        self.frontLeft_controller.reset()
        self.frontRight_controller.reset()

        return self._state

    def execute(self):

        currentWheelSpeeds = wpimath.kinematics.MecanumDriveWheelSpeeds(
            self.drive_FrontLeftEncoder.getRate(),
            self.drive_FrontRightEncoder.getRate(),
            self.drive_FrontLeftEncoder.getRate(),
            self.drive_FrontRightEncoder.getRate()
        )

        self._odometry.update(
            Rotation2d.fromDegrees(-self.gyro.getAngle()),
            currentWheelSpeeds
        )

        if not self._state:
            return

        now = self._timer.get()
        last_tm = self._lastTm
        dt = now - last_tm

        if last_tm < 0:
            self.drivetrain.tank_move(0, 0)
            self._lastTm = now
            return

        targetWheelSpeeds = self._kinematics.toWheelSpeeds(
            self._controller.calculate(
                self._odometry.getPose(), self._trajectory.sample(now)
            )
        )

        prevSpeeds = self._prevSpeeds

        fl_ff = self._ff.calculate(
            targetWheelSpeeds.frontLeft, (targetWheelSpeeds.frontLeft - prevSpeeds.frontLeft) / dt
        )
        fr_ff = self._ff.calculate(
            targetWheelSpeeds.frontRight, (targetWheelSpeeds.frontRight - prevSpeeds.frontRight) / dt
        )

        fl_v = (
            self.frontLeft_controller.calculate(
                self.drive_FrontLeftEncoder.getRate(), targetWheelSpeeds.frontLeft
            )
            + fl_ff
        )
        fr_v = (
            self.frontRight_controller.calculate(
                self.drive_FrontRightEncoder.getRate(), targetWheelSpeeds.frontRight
            )
            + fr_ff
        )
        print(fl_v, fr_v)

        self.drivetrain.tank_move(fl_v, fr_v)

        if now > self._trajectory.totalTime():
            self._state.done = True
            self._state = None
            print("final pose", self._odometry.getPose())
        else:
            self._lastTm = now
            self._prevSpeeds = targetWheelSpeeds
