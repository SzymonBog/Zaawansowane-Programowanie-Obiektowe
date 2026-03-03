from abc import ABC, abstractmethod


class Pizza:
    def __init__(self):
        self.ingredients = []


class Builder(ABC, Pizza):
    _ingredients: list

    @abstractmethod
    def add_cheese(self):
        pass

    @abstractmethod
    def add_salami(self):
        pass

    @abstractmethod
    def add_mushrooms(self):
        pass

    @abstractmethod
    def add_onion(self):
        pass


class PizzaBuilder(Builder):
    def __init__(self, pizza_type: str):
        super().__init__()
        self.type = pizza_type

    def add_cheese(self):
        self.ingredients.append("cheese")

    def add_salami(self):
        if self.type != "vege":
            self.ingredients.append("salami")
        else:
            print("It's a vege pizza")

    def add_mushrooms(self):
        self.ingredients.append("mushrooms")

    def add_onion(self):
        self.ingredients.append("onion")


pb = PizzaBuilder("vege")
pb.add_cheese()
pb.add_mushrooms()
pb.add_onion()
pb.add_salami()
print(pb.ingredients)


class Computer:
    def __init__(self, ram, ram_memory, processor, processor_cores, year, has_cd_rom, screen, is_keyboard_rgb, number_of_usb_ports):
        self.ram = ram
        self.ram_memory = ram_memory
        self.processor = processor
        self.processor_cores = processor_cores
        self.year = year
        self.has_cd_rom = has_cd_rom
        self.screen = screen
        self.is_keyboard_rgb = is_keyboard_rgb
        self.number_of_usb_ports = number_of_usb_ports


class PCBuilder(ABC):
    @abstractmethod
    def set_ram(self, ram: str):
        pass

    @abstractmethod
    def set_ram_memory(self, memory: int):
        pass

    @abstractmethod
    def set_processor(self, cpu: str):
        pass

    @abstractmethod
    def set_processor_cores(self, cores: int):
        pass

    @abstractmethod
    def set_year(self, y: int):
        pass

    @abstractmethod
    def set_has_cd_rom(self, has: bool):
        pass

    @abstractmethod
    def set_screen(self, model: str):
        pass

    @abstractmethod
    def set_is_keyboard_rgb(self, rgb: bool):
        pass

    @abstractmethod
    def set_number_of_usb_ports(self, number: int):
        pass


class ComputerBuilder(PCBuilder):
    computer: Computer

    def __init__(self, computer):
        self.computer = computer

    def set_ram(self, ram: str):
        self.computer.ram = ram

    def set_ram_memory(self, memory: int):
        self.computer.ram_memory = memory

    def set_processor(self, cpu: str):
        self.computer.processor = cpu

    def set_processor_cores(self, cores: int):
        self.computer.processor_cores = cores

    def set_year(self, y: int):
        self.computer.year = y

    def set_has_cd_rom(self, has: bool):
        self.computer.has_cd_rom = has

    def set_screen(self, model: str):
        self.computer.screen = model

    def set_is_keyboard_rgb(self, rgb: bool):
        self.computer.is_keyboard_rgb(rgb)

    def set_number_of_usb_ports(self, number: int):
        self.computer.number_of_usb_ports = number


pc = ComputerBuilder(Computer)
pc.set_ram("2345")
print(pc.computer.ram)
