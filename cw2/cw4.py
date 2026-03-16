from copy import deepcopy, copy
from typing import Any


class CharacterPrototype:
    def __init__(self, lvl: int, hp: float, weapons: dict, powers: dict, chestplate: str, helmet: str, function: str, **kwargs: dict) -> None:
        self.lvl = lvl
        self.hp = hp
        self.weapons = weapons
        self.powers = powers
        self.chestplate = chestplate
        self.helmet = helmet
        self.function = function

        for key in kwargs:
            setattr(self, key, kwargs[key])

    def __str__(self) -> str:
        summary = []

        for key, val in vars(self).items():
            summary.append(f"{key}: {val}\n")

        return "".join(summary)


class Prototype:
    def __init__(self) -> None:
        self.objects = dict()

    def add_prototype(self, id_: int, obj: Any) -> None:
        self.objects[id_] = obj

    def del_prototype(self, id_: int) -> None:
        del self.objects[id_]

    def deep_copy(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = deepcopy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])

            return instance
        else:
            raise ModuleNotFoundError("ID not found!")

    def shallow_copy(self, id_: int, **kwargs: dict) -> Any:
        if id_ in self.objects:
            instance = copy(self.objects[id_])

            for key in kwargs:
                setattr(instance, key, kwargs[key])

            return instance
        else:
            raise ModuleNotFoundError("ID not found!")


Mage = CharacterPrototype(12, 1200, {"primary": "Wand"}, {"primary": "Fireball"}, "Iron", "Iron", "Mage")
Warrior = CharacterPrototype(10, 1000, {"primary": "Sword", "Secondary": "Battle Axe"}, {}, "Steel", "Steel", "Warrior")

print(Mage)
print(Warrior)

prototypes = Prototype()
prototypes.add_prototype(1, Mage)
secondMage = prototypes.deep_copy(1)
thirdMage = prototypes.shallow_copy(1)

prototypes.add_prototype(2, Warrior)
secondWarrior = prototypes.deep_copy(2, chestplate="dark steel")

Mage.powers.update({"second": "Dark Energy"})

print(secondMage)
print(thirdMage)

print(secondWarrior)
# A, B
