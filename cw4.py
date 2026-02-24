from dataclasses import dataclass, field


@dataclass(frozen=False)
class Product:
    name: str
    price: float
    category: str = field(default="General")
    """
    #post_init
    if self.price <= 0:
        ValueError("Price has to be greater than 0")
    """


p = Product("Juice", -5, "Drinks")

