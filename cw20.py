from abc import ABC, abstractmethod


class Instrument(ABC):
    @abstractmethod
    def play(self):
        pass


class Piano(Instrument):
    def play(self):
        print("AFCDACFDCF DCGDAFGDCA")


class Guitar(Instrument):
    def play(self):
        print("AECGDA BF#DAEB FFFCDG")


p = Piano()
g = Guitar()
p.play()
g.play()
