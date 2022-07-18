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

    shooter_timer: wpilib.Timer

    @magicbot.state()
    def shooter_shoot(self):
        """
        @param1 state: shooter'i calistirmak icin True, Kapatmak icin False
        """
        self.shooter_front1.set(ctre.ControlMode.PercentOutput, self._intake_valueFront)
        self.shooter_front1.set(ctre.ControlMode.PercentOutput, self._intake_valueFront)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, self._intake_valueRear)

    magicbot.state()
    def shooter_stop(self):
        """
        @param1 state: shooter'i calistirmak icin True, Kapatmak icin False
        """
        self.shooter_front1.set(ctre.ControlMode.PercentOutput, 0)
        self.shooter_front1.set(ctre.ControlMode.PercentOutput, 0)
        self.shooter_rear.set(ctre.ControlMode.PercentOutput, 0)

    def shooter_begin(self, _valueFront: float, _valueRear: float):
        self._intake_valueFront = _valueFront
        self._intake_valueRear =  _valueRear
        self.engage("start_shooterAlgorithym")    

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
                        self.next_state("shooter_shoot")
                    else:
                        self.shooter_timer.stop()
                        self.shooter_timer.reset()
                        self.next_state("shooter_stop")
                        self.ballCount -= 1
                        self.shooterRunning = False
