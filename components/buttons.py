import wpilib
from wpilib import SmartDashboard as sd

class ButtonCtrl:

    #Bu zimbirtilari buraya tasidim, robot.pyda olmalarinin bir anlami yok smartdashboard kullandigimiz icin

    flightStick: wpilib.Joystick

    shooterMode = {0: "Lower Hub Dipdibe",
                   1: "Lower Hub",
                   2: "Upper Hub",
                   3: "Upper Hub 2 Metre"}
    
    shooter_speedChange_value = 0
    shooter_speedChanged = False

    def climb_control(self):
        self.climbMotor1_LowInput = self.flightStick.getRawButton(4)
        self.climbMotor1_UpInput = self.flightStick.getRawButton(5)
        self.climbMotor2_LowInput = self.flightStick.getRawButton(6)
        self.climbMotor2_UpInput = self.flightStick.getRawButton(7)
        
        if self.climbMotor1_LowInput:
            sd.putNumber("climbMotor1",-1)
        elif self.climbMotor1_UpInput:
            sd.putNumber("climbMotor1",1)
        else:
            sd.putNumber("climbMotor1",0)

        if self.climbMotor2_LowInput:
            sd.putNumber("climbMotor2",-1)
        elif self.climbMotor2_UpInput:
            sd.putNumber("climbMotor2",1)
        else:
            sd.putNumber("climbMotor2",0)
    
    def intake_shooter_control(self):
        self.intake_driverInput = self.flightStick.getRawButton(2)
        self.shooter_driverInput = self.flightStick.getRawButton(1)
        self.shooter_changeSpeed_Input = self.flightStick.getRawButtonPressed(3)

        if self.intake_driverInput:
            sd.putString("shooterState","Inactive")
            sd.putBoolean("intakeRunning", True)
            sd.putBoolean("shooterRunning", False)

        
        if self.shooter_driverInput:
            sd.putString("IntakeState","Inactive")
            sd.putBoolean("intakeRunning", False)
            sd.putBoolean("shooterRunning", True)
        
        if self.shooter_changeSpeed_Input:
            if self.shooter_speedChange_value < 3:
                self.shooter_speedChange_value += 1
            else:
                self.shooter_speedChange_value = 0
            self.shooter_speedChanged = True

    def shooter_speed_configuration(self):

        if self.shooter_speedChange_value == 0:
            sd.putNumber("shooter_valueFront", 0.5)
            sd.putNumber("shooter_valueRear", 0.5)
            
        if self.shooter_speedChange_value == 1:
            sd.putNumber("shooter_valueFront", 1)
            sd.putNumber("shooter_valueRear", 0.5)
        
        if self.shooter_speedChange_value == 2:
            sd.putNumber("shooter_valueFront", 0.5)
            sd.putNumber("shooter_valueRear", 1)
        
        if self.shooter_speedChange_value == 3:
            sd.putNumber("shooter_valueFront", 1)
            sd.putNumber("shooter_valueRear", 1)

        if self.shooter_speedChanged:
            self.shooter_speedChanged = False

            for i in self.shooterMode:
                _state = (i == self.shooter_speedChange_value)
                sd.putBoolean(self.shooterMode.get(i), _state)

    def atis_kontrol(self):
        range = sd.getNumber("hubDistance", 0)
        tolerance = 0.2
        if self.shooter_speedChange_value == 0:
            goal = 0.5
        elif self.shooter_speedChange_value == 1:
            goal = 1
        elif self.shooter_speedChange_value == 2:
            goal = 3
        elif self.shooter_speedChange_value == 3:
            goal = 2
        if ((range-tolerance) < goal) and ((range+tolerance) > goal):
            sd.putBoolean("atis_Kontrol",True)
        else:
            sd.putBoolean("atis_Kontrol",False)

    def execute(self):
        self.atis_kontrol()
        self.climb_control()
        self.intake_shooter_control()
        self.shooter_speed_configuration()
