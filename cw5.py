from datetime import datetime


class Car:
    def __init__(self, brand, model, year):
        self.brand = brand
        self.model = model
        self.year = year

    def is_classic(self):
        if self.year + 25 <= datetime.now().year:
            return True
        else:
            return False


c1 = Car("Nissan", "Leaf", 2020)
c2 = Car("Fiat", "Seicento", 1998)

print(c1.is_classic())
print(c2.is_classic())
