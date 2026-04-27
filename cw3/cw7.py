from abc import ABC
from random import choice


class Icon(ABC):
    def __init__(self, name: str, pixels: tuple) -> None:
        self.name = name
        self.pixels = pixels

    def draw(self, x, y):
        print(f"Drawing '{self.name}' icon at ({x}, {y})")


class ExitIcon(Icon):
    pass


class MinimizeIcon(Icon):
    pass


class OpenNewIcon(Icon):
    pass


class IconFactory:
    @staticmethod
    def get_icon(name: str, pixels: tuple) -> Icon:
        match name:
            case "exit":
                return ExitIcon(name, pixels)
            case "minimize":
                return MinimizeIcon(name, pixels)
            case "open":
                return OpenNewIcon(name, pixels)
            case _:
                raise ValueError(f"Unknown icon type: {name}")


names = ("exit", "minimize", "open", "exit")
pixels = ("20x20", "25x25", "40x20", "100x100")


class UserInterface:
    icons: list

    def __init__(self) -> None:
        self.icons = []

    def generate_icons(self) -> None:
        for _ in range(12):
            name = self.get_random_name()
            pixel = self.get_random_pixels()

            ic = IconFactory.get_icon(name, pixel)

            self.icons.append(ic)

    def get_random_name(self) -> str:
        return choice(names)

    def get_random_pixels(self) -> tuple:
        return choice(pixels)


ui = UserInterface()
ui.generate_icons()

for icon in ui.icons:
    print(f"object ID: {id(icon)} name ID: {id(icon.name)}, pixels ID: {id(icon.pixels)}")


# ------------------------------------------------------------


class ProductLabel(ABC):
    def __init__(self, name: str, barcode: str) -> None:
        self.name = name
        self.barcode = barcode


class Juice(ProductLabel):
    pass

class Cookie(ProductLabel):
    pass

class Coffee(ProductLabel):
    pass

class Candy(ProductLabel):
    pass


class ProductFactory:
    _labels = {}

    @classmethod
    def get_label(cls, name: str, barcode: str) -> str:
        key = (name, barcode)
        if key not in cls._labels:
            match name:
                case "Juice":
                    cls._labels[key] = Juice(name, barcode)
                case "Cookie":
                    cls._labels[key] = Cookie(name, barcode)
                case "Coffee":
                    cls._labels[key] = Coffee(name, barcode)
                case "Candy":
                    cls._labels[key] = Candy(name, barcode)
                case _:
                    raise ValueError(f"Unknown product: {name}")
        return cls._labels[key]


class Product:
    def __init__(self, name: str, barcode: str, shelf: int, position: float) -> None:
        self.label = ProductFactory.get_label(name, barcode)
        self.shelf = shelf
        self.position = position

    def __repr__(self) -> str:
        return f"Product: {self.label.name} ({self.label.barcode}, {self.shelf}, {self.position})"


warehouse = []

for i in range(10000):
    warehouse.append(Product("Juice", "59012345", i, i%10))

for i in range(10000):
    warehouse.append(Product("Cookie", "84566485", i, i%10))

print(warehouse[0], warehouse[10000])
print(f"Liczba etykiet w pamięci: {len(ProductFactory._labels)}")


# ---------------------------------------------------------


class Color:
    def __init__(self, r, g, b):
        self.r = r
        self.g = g
        self.b = b

class ColorFactory:
    _colors = {}

    @classmethod
    def get_color(cls, r, g, b):
        rgb = (r, g, b)
        if rgb not in cls._colors:
            cls._colors[rgb] = Color(r, g, b)
        return cls._colors[rgb]

class Pixel:
    def __init__(self, x, y, color_obj):
        self.x = x
        self.y = y
        self.color = color_obj

red = ColorFactory.get_color(255, 0, 0)
canvas = []

for x in range(100):
    for y in range(100):
        canvas.append(Pixel(x, y, red))

print(f"Created {len(canvas)} pixels.")
print(f"Number of Colors in memory: {len(ColorFactory._colors)}")
