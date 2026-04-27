import math
from abc import ABC, abstractmethod
from random import choice



def calculate_tax_pl(product):
    tax = products[product] * 0.19
    return tax


def calculate_tax_rus(product):
    tax = products[product] * 0.45
    return tax


def calculate_tax_usa(product):
    tax = products[product] * 0.27
    return tax


def calculate_tax_strategy(country, list_) -> float:
    tax_amount = 0
    if country == "Poland":
        for p in list_:
            tax_amount += calculate_tax_pl(p)
        return tax_amount
    elif country == "Russia":
        for p in list_:
            tax_amount += calculate_tax_rus(p)
        return tax_amount
    elif country == "USA":
        for p in list_:
            tax_amount += calculate_tax_usa(p)
        return tax_amount


products = {
    "juice": 4,
    "orange": 1.5,
    "tomato": 1.75,
    "water": 1.8,
    "chocolate": 5,
    "ice cubes": 2.1
}

to_buy = ["juice", "chocolate", "orange"]

print(calculate_tax_strategy("Poland", to_buy))
print(calculate_tax_strategy("USA", to_buy))
print(calculate_tax_strategy("Russia", to_buy))


# ---------------------------------------------------------------------------------


class Strategy(ABC):
    health: float
    damage: float
    position: tuple
    attack_range: float
    walk_range: float

    instances = []

    def __init__(self) -> None:
        self.health = None
        self.damage = None
        self.position = None
        self.walk_range = None
        self.attack_range = None
        Strategy.instances.append(self)

    @abstractmethod
    def move(self, place: tuple) -> None:
        pass

    @abstractmethod
    def attack(self) -> None:
        pass


class Knight(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.health = 200
        self.damage = 100
        self.walk_range = 4
        self.attack_range = 1

    def move(self, place: tuple) -> None:
        dif = math.sqrt((self.position[0] - place[0])^2 + (self.position[1] - place[1])^2)
        if dif <= self.walk_range:
            if (0, 0) <= place <= (15, 15):
                self.position = place
                self.attack()
            else:
                print("Pick valid spot")

    def attack(self) -> None:
        print(Strategy.__subclasses__())
        return


class Berserker(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.health = 50
        self.damage = 300
        self.walk_range = 8
        self.attack_range = 2

    def move(self, place: tuple) -> None:
        dif = math.sqrt((self.position[0] - place[0])^2 + (self.position[1] - place[1])^2)
        if dif <= self.walk_range:
            if (0, 0) <= place <= (15, 15):
                self.position = place
                self.attack()
            else:
                print("Pick valid spot")

    def attack(self) -> None:
        sub = Strategy.instances
        for s in sub:
            print(s)
        return


b = Berserker()
b1 = Berserker()
b1.attack()
k = Knight()
k.attack()
