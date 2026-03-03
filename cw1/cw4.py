from dataclasses import dataclass, field


@dataclass(frozen=False)
class Product:
    name: str
    price: float
    category: str = field(default="General")

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price has to be greater than 0")


p1 = Product("Juice", 5, "Drinks")
p2 = Product("Juice", -5, "Drinks")
