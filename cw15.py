class GameCharacter:
    default_health = 100

    def __init__(self):
        self.health = self.default_health

    def restore_health(self):
        self.health = self.default_health

    @classmethod
    def set_default_health(cls, new_value):
        cls.default_health = new_value
