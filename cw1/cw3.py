from dataclasses import dataclass, field


@dataclass(frozen=False)
class Book:
    title: str
    author: str
    year: int
    price: float

    def apply_discount(self, discount_pct: float):
        self.price = self.price * (1 - (discount_pct / 100))

    def get_string(self):
        return self.title + " " + self.author + " " + str(self.year) + " " + str(self.price)


b = Book("IT", "Stephen King", 2013, 100)
print(b.get_string())
b.apply_discount(33)
print(b.get_string())
b.apply_discount(50)
print(b.get_string())
