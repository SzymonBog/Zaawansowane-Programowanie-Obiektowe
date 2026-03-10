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


class TeslaFactory(Factory):  # add BMW
    def produce_wheels(self, diameter: int, amount: int) -> tuple:
        return tuple([Wheel(diameter=diameter) for _ in range(amount)])

    def produce_body(self, color: str, body_type: str) -> Body:
        b_t = ["Sedan", "SUV"]
        if body_type not in b_t:
            raise ValueError("This factory only uses body of 'Sedan' and 'SUV'")
        else:
            return Body(color=color, body_type=body_type)

    def produce_doors(self, interior_material: str, amount: int) -> tuple:
        return tuple([Door(interior_material=interior_material) for _ in range(amount)])

    def produce_seats(self, material: str, amount: int) -> tuple:
        return tuple([Seat(material=material) for _ in range(amount)])


class BMWFactory(Factory):  # add BMW
    def produce_wheels(self, diameter: int, amount: int) -> tuple:
        return tuple([Wheel(diameter=diameter) for _ in range(amount)])

    def produce_body(self, color: str, body_type: str) -> Body:
        b_t = ["Sedan", "SUV"]
        if body_type not in b_t:
            raise ValueError("This factory only uses body of 'Sedan' and 'SUV'")
        else:
            return Body(color=color, body_type=body_type)

    def produce_doors(self, interior_material: str, amount: int) -> tuple:
        return tuple([Door(interior_material=interior_material) for _ in range(amount)])

    def produce_seats(self, material: str, amount: int) -> tuple:
        return tuple([Seat(material=material) for _ in range(amount)])


class HatchbackCarFactory(Factory):  # add BMW
    def produce_wheels(self, diameter: int, amount: int) -> tuple:
        return tuple([Wheel(diameter=diameter) for _ in range(amount)])

    def produce_body(self, color: str, body_type: str) -> Body:
        b_t = ["Sedan", "SUV"]
        if body_type not in b_t:
            raise ValueError("This factory only uses body of 'Sedan' and 'SUV'")
        else:
            return Body(color=color, body_type=body_type)

    def produce_doors(self, interior_material: str, amount: int) -> tuple:
        return tuple([Door(interior_material=interior_material) for _ in range(amount)])

    def produce_seats(self, material: str, amount: int) -> tuple:
        return tuple([Seat(material=material) for _ in range(amount)])


class AbstractFactory:
    @staticmethod
    def get_factory(model: Any) -> Any:
        match model:
            case "Tesla":
                return TeslaFactory()
            case "BMW":
                return BMWFactory()
            case "HatchbackCar":
                return HatchbackCarFactory()
            case _:
                raise ValueError("Incorrect car model")


@dataclass
class Car:
    wheels: tuple
    body: Body
    doors: tuple
    seats: tuple
    body_type: str


class CarManufacturer(ABC):
    client_options: dict

    def __init__(self, client_options: dict) -> None:
        self.client_options = client_options

    def produce_car(self) -> Car:
        factory = AbstractFactory.get_factory(self.client_options["model"])
        wheels, body, doors, seats, body_type = self._request_parts(factory)

        return Car(wheels=wheels, body=body, doors=doors, seats=seats, body_type=body_type)

    def _request_parts(self, factory: Any) -> tuple:
        wheels = factory.produce_wheels(self.client_options["diameter"], 4)
        body_type = self.client_options["body_type"]
        body = factory.produce_body(self.client_options["color"], body_type)
        doors = factory.produce_doors(self.client_options["doors"], 5)
        seats = factory.produce_seats(self.client_options["seats"], 5)

        return wheels, body, doors, seats, body_type


class Client:
    @staticmethod
    def request_car(request: dict) -> Car:
        manufacturer = CarManufacturer(request)
        new_car = manufacturer.produce_car()

        return new_car


car_specs1 = {
    "model": "Tesla",
    "diameter": 18,
    "color": "black",
    "doors": "plastic",
    "seats": "normal",
    "body_type": "SUV"
}

car_specs2 = {
    "model": "BMW",
    "diameter": 18,
    "color": "black",
    "doors": "plastic",
    "seats": "normal",
    "body_type": "Sedan"
}

car_specs3 = {
    "model": "HatchbackCar",
    "diameter": 18,
    "color": "black",
    "doors": "plastic",
    "seats": "normal",
    "body_type": "Sedan"
}

client = Client()
car1 = client.request_car(car_specs1)
car2 = client.request_car(car_specs2)
car3 = client.request_car(car_specs3)
print(car1)
print(car2)
print(car3)


# --------------------------------------------------------------------------


@dataclass
class Screen:
    resolution: float


@dataclass
class CPU:
    model: str


@dataclass
class Camera:
    quality: str


class PhoneFactory(ABC):
    @abstractmethod
    def check_model(self, model: str):
        pass

    @abstractmethod
    def produce_screen(self, resolution: float) -> Screen:
        pass

    @abstractmethod
    def produce_cpu(self, model: str) -> CPU:
        pass

    @abstractmethod
    def produce_camera(self, quality: str) -> Camera:
        pass


class ApfelPhoneFactory(PhoneFactory):
    def check_model(self, model: str):
        models = ["Mak", "I", "MI"]
        if model not in models:
            raise ValueError("We don't produce this model")

    def produce_screen(self, resolution: float) -> Screen:
        return Screen(resolution=resolution)

    def produce_cpu(self, model: str) -> CPU:
        return CPU(model=model)

    def produce_camera(self, quality: str) -> Camera:
        return Camera(quality=quality)


class SzajsungPhoneFactory(PhoneFactory):
    def check_model(self, model: str):
        models = ["A55", "S9", "Ace8"]
        if model not in models:
            raise ValueError("We don't produce this model")

    def produce_screen(self, resolution: float) -> Screen:
        return Screen(resolution=resolution)

    def produce_cpu(self, model: str) -> CPU:
        return CPU(model=model)

    def produce_camera(self, quality: str) -> Camera:
        return Camera(quality=quality)


class MajfonPhoneFactory(PhoneFactory):
    def check_model(self, model: str):
        models = ["21", "20", "19"]
        if model not in models:
            raise ValueError("We don't produce this model")

    def produce_screen(self, resolution: float) -> Screen:
        return Screen(resolution=resolution)

    def produce_cpu(self, model: str) -> CPU:
        return CPU(model=model)

    def produce_camera(self, quality: str) -> Camera:
        return Camera(quality=quality)


class AbstractPhoneFactory:
    @staticmethod
    def get_factory(model: Any) -> Any:
        match model:
            case "Apfel":
                return ApfelPhoneFactory()
            case "Szajsung":
                return SzajsungPhoneFactory()
            case "Majfon":
                return MajfonPhoneFactory()
            case _:
                raise ValueError("Incorrect phone model")


@dataclass
class Phone:
    model: str
    screen: float
    cpu: str
    camera: str


class PhoneManufacturer(ABC):
    client_options: dict

    def __init__(self, client_options: dict) -> None:
        self.client_options = client_options
