import magicbot
from components.aimbot import AimBot

class Deneme(magicbot.AutonomousStateMachine):

    MODE_NAME = "Hub'a yaklas"
    DEFAULT = False

    aimbot: AimBot

    @magicbot.state(first=True)
    def aim(self):
        self.aimbot.aim(3)
