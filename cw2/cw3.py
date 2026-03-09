import enum
from abc import ABC, abstractmethod
from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Wheel:
    diameter: int
    material: str = field(default="aluminium")


@dataclass
class Body:
    body_type: str
    color: str
    thickness: float = field(default=.6)


@dataclass
class Door:
    interior_material: str
    control: str = field(default="manual")


@dataclass
class Seat:
    material: str
    control: str = field(default="manual")


@dataclass
class PremiumSticker:
    icon: str
    color: str


class Factory(ABC):
    @abstractmethod
    def produce_wheels(self, diameter: int, amount: int) -> tuple:
        pass

    @abstractmethod
    def produce_body(self, color: str, body_type: str) -> Body:
        pass

    @abstractmethod
    def produce_doors(self, interior_material: str, amount: int) -> tuple:
        pass

    @abstractmethod
    def produce_seats(self, material: str, amount: int) -> tuple:
        pass


class TeslaFactory(Factory): # BMW
    def produce_wheels(self, diameter: int, amount: int) -> tuple:
        return tuple([Wheel(diameter=diameter) for _ in range(amount)])

    def produce_body(self, color: str, body_type: str) -> Body:
        return Body(color=color) # ?????????????????????????????

    def produce_doors(self, interior_material: str, amount: int) -> tuple:
        return tuple([Door(interior_material=interior_material) for _ in range(amount)])

    def produce_seats(self, material: str, amount: int) -> tuple:
        return tuple([Seat(material=material) for _ in range(amount)])
