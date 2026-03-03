from abc import ABC, abstractmethod


class Vehicle(ABC):
    @abstractmethod
    def max_speed(self, new_max):
        pass


class Car(Vehicle):
    def __init__(self):
        self.max_vel = 0

    def max_speed(self, new_max):
        self.max_vel = new_max


class Bicycle(Vehicle):
    def __init__(self):
        self.max_vel = 0

    def max_speed(self, new_max):
        self.max_vel = new_max


c = Car()
b = Bicycle()
c.max_speed(220)
b.max_speed(25)
