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
        Strategy.instances.append(self)

    @abstractmethod
    def attack(self) -> None:
        pass


class Knight(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.health = 200
        self.damage = 100

    def attack(self) -> None:
        cl = Strategy.__subclasses__()
        print(cl)
        for c in cl:
            if c != self.__class__:
                print(c.instances)
        return


class Berserker(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.health = 50
        self.damage = 300

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


# ------------------------------------------------------------------------


def bubble_sort(list_):
    print("Bubble sort")
    return sorted(list_)


def selection_sort(list_):
    print("Selection sort")
    return sorted(list_)


def quick_sort(list_):
    print("Quick sort")
    return sorted(list_)


def sort_list_strategy(list_):
    if len(list_) <= 10:
        return bubble_sort(list_)
    elif len(list_) <= 15:
        return selection_sort(list_)
    else:
        return quick_sort(list_)


list_1 = [5, 3, 6, 4, 2, 3, 0, 5, 8, 6]
list_2 = [x ** 2 * (-1) ** x for x in range(1, 15)]
list_3 = [2 * (-x) ** x + 1 for x in range(1, 20)]

print(list_1)
print(list_2)
print(list_3)
print(sort_list_strategy(list_1))
print(sort_list_strategy(list_2))
print(sort_list_strategy(list_3))
