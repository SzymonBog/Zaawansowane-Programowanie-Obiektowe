class FlyingVehicle:
    def move(self):
        return "I fly"


class WaterVehicle:
    def move(self):
        return "I sail"


class AmphibiousVehicle(FlyingVehicle, WaterVehicle):
    def __init__(self):
        self.mode = "air"

    def change_mode(self):
        if self.mode == "air":
            self.mode = "water"
        else:
            self.mode = "air"

    def move(self):
        if self.mode == "air":
            return "I fly"
        else:
            return "I sail"


fv = FlyingVehicle()
wv = WaterVehicle()
av = AmphibiousVehicle()
print(f"{fv.move()} {wv.move()} {av.move()}")
av.change_mode()
print(f"{av.move()}")
av.change_mode()
print(f"{av.move()}")
av.change_mode()
print(f"{av.move()}")
av.change_mode()
print(f"{av.move()}")
