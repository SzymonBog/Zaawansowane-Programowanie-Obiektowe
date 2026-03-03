from abc import ABC, abstractmethod
from math import pi


class Shape(ABC):
    @abstractmethod
    def area(self):
        pass


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        a = self.radius * self.radius * pi
        return a


class Rectangle(Shape):
    def __init__(self, side_a, side_b):
        self.side_a = side_a
        self.side_b = side_b

    def area(self):
        a = self.side_a * self.side_b
        return a


c = Circle(10)
r = Rectangle(26, 15)
print(c.area())
print(r.area())
