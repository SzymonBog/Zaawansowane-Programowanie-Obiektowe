class Animal:
    def make_sound(self):
        return "Some sound"


class Pet:
    def is_domestic(self):
        return True


class Dog(Animal, Pet):
    def make_sound(self):
        return "Woof woof"

    """
    def is_domestic(self):
        return True
    """


a = Animal()
p = Pet()
d = Dog()
print(f"{a.make_sound()} {p.is_domestic()} {d.make_sound()} {d.is_domestic()}")
