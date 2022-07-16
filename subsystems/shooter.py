import wpilib
import ctre
import magicbot

class Shooter(magicbot.StateMachine):
    belt_upper: ctre.VictorSPX
    belt_lower: ctre.VictorSPX

    switch_upper: wpilib.DigitalInput
    switch_lower: wpilib.DigitalInput

    shooter_front1: ctre.VictorSPX
    shooter_front2: ctre.VictorSPX
    shooter_rear: ctre.VictorSPX

    ballCount: int

    intakeRunning: bool
    shooterRunning: bool

    smart_dashboard: wpilib.SmartDashboard

    shooter_timer: wpilib.Timer

    def shooter_begin(self, _valueFront: float, _valueRear: float):
        self._intake_valueFront = _valueFront
        self._intake_valueRear =  _valueRear
        self.engage("start_shooterAlgorithym")


    def shooter_shoot(self, state: bool):
        """
        @param1 state: shooter'i calistirmak icin True, Kapatmak icin False
        """
        if state:
            self.shooter_front1.set(ctre.ControlMode.PercentOutput, self._intake_valueFront)
            self.shooter_front1.set(ctre.ControlMode.PercentOutput, self._intake_valueFront)
            self.shooter_rear.set(ctre.ControlMode.PercentOutput, self._intake_valueRear)
        else:
            self.shooter_front1.set(ctre.ControlMode.PercentOutput, 0)
            self.shooter_front1.set(ctre.ControlMode.PercentOutput, 0)
            self.shooter_rear.set(ctre.ControlMode.PercentOutput, 0)    

    @magicbot.state(first=True)
    def start_shooterAlgorithym(self):
        if self.shooterRunning:
            if self.ballCount >= 1 and not self.intakeRunning:
                if not self.switch_upper.get():
                    self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
                    self.shooterRunning = True
                else:
                    self.shooter_timer.start()
                    self.belt_upper.set(ctre.ControlMode.PercentOutput, 1)
                    if not self.shooter_timer.hasPeriodPassed(3):
                        self.shooter_shoot(True)
                    else:
                        self.shooter_timer.stop()
                        self.shooter_timer.reset()
                        self.shooter_shoot(False)
                        self.ballCount -= 1
                        self.shooterRunning = False


    def execute(self):
        self.start_shooterAlgorithym()