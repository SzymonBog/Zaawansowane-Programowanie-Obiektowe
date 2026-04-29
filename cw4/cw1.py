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
        self.damage = 20

    def attack(self) -> None:
        if self.health > 0:
            cl = Strategy.__subclasses__()
            print(cl)
            for c in cl:
                if c != self.__class__:
                    print(c.instances)
                    for i in c.instances:
                        if i.health > 0:
                            ch = choice(["Miss", "Hit", "Crit"])
                            if ch == "Miss":
                                print("Missed")
                            elif ch == "Hit":
                                i.health -= self.damage
                                print(i.health)
                            elif ch == "Crit":
                                i.health -= self.damage * 2
                                print(i.health)


class Berserker(Strategy):
    def __init__(self) -> None:
        super().__init__()
        self.health = 50
        self.damage = 75

    def attack(self) -> None:
        if self.health > 0:
            cl = Strategy.__subclasses__()
            print(cl)
            for c in cl:
                if c != self.__class__:
                    print(c.instances)
                    for i in c.instances:
                        if i.health > 0:
                            ch = choice(["Miss", "Hit", "Crit"])
                            if ch == "Miss":
                                print("Missed")
                            elif ch == "Hit":
                                i.health -= self.damage
                                print(i.health)
                            elif ch == "Crit":
                                i.health -= self.damage * 2
                                print(i.health)


b0 = Berserker()
b1 = Berserker()
b2 = Berserker()
b3 = Berserker()

k0 = Knight()
k1 = Knight()
k2 = Knight()
k3 = Knight()

kn = [k0, k1, k2, k3]
ka = 4
br = [b0, b1, b2, b3]
ba = 4

r = 1

while True:
    print(f"Round {r}")

    for i in range(8):
        if i % 2 == 0:
            br[int(i/2)].attack()
        else:
            kn[int((i-1)/2)].attack()

    # for k in kn:
    #    k.attack()

    for k in kn:
        if k.health <= 0:
            ka -= 1

    if ka == 0:
        print("Berserkers won")
        break

    for b in br:
        if b.health <= 0:
            ba -= 1

    if ba == 0:
        print("Knights won")
        break

    r += 1

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
