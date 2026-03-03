class ElectricVehicle:
    def fuel_type(self):
        return "electric"


class GasolineVehicle:
    def fuel_type(self):
        return "gasoline"


class HybridCar(ElectricVehicle, GasolineVehicle):
    def fuel_type(self):
        return "hybrid"


ev = ElectricVehicle()
print(ev.fuel_type())

gv = GasolineVehicle()
print(gv.fuel_type())

hv = HybridCar()
print(hv.fuel_type())
