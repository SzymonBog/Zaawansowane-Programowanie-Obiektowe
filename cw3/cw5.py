from abc import ABC, abstractmethod


class Document(ABC):
    file: str

    def __init__(self, file: str) -> None:
        self.file = file

    @abstractmethod
    def render_file(self) -> str:
        pass

    @abstractmethod
    def theme(self) -> None:
        pass


class LightThemeRenderer(Document):
    file: str

    def render_file(self) -> str:
        return self.file

    def theme(self) -> str:
        return "Light Theme"


class DarkThemeRenderer(Document):
    file: str

    def render_file(self) -> str:
        return self.file[:50]

    def theme(self) -> str:
        return "Dark Theme"


class Renderer(ABC):
    renderer: Document

    def __init__(self, renderer: Document) -> None:
        self.renderer = renderer

    @abstractmethod
    def read_file(self) -> str:
        pass


class LightPage(Renderer):
    renderer: Document

    def read_file(self) -> str:
        theme = self.renderer.theme()
        content = self.renderer.render_file()

        return f"theme: {theme}\n{content}"


class DarkPage(Renderer):
    renderer: Document

    def read_file(self) -> str:
        theme = self.renderer.theme()
        content = self.renderer.render_file()

        return f"theme: {theme}\n{content}"


article1 = "Spektakularny sukces Adama Miłosza. Po raz kolejny przeskoczył skocznię w Wiśle. Czy czeka nas powrót wielkiego mistrza?"
article2 = "Tele duperele"

renderer1 = DarkThemeRenderer(article1)
renderer2 = LightThemeRenderer(article2)

dark_page = DarkPage(renderer1)
light_page = LightPage(renderer2)

print(dark_page.read_file())
print(light_page.read_file())


# ---------------------------------------------------------------------------


class RemoteControl(ABC):
    device: str
    
    def __init__(self, device: str) -> None:
        self.device = device

    @abstractmethod
    def turn_on(self) -> str:
        pass

    @abstractmethod
    def turn_off(self) -> str:
        pass

    @abstractmethod
    def change_channel(self, num) -> str:
        pass

    @abstractmethod
    def change_station(self, freq) -> str:
        pass

    @abstractmethod
    def fly(self, direction) -> str:
        pass


class TVController(RemoteControl):
    device: str

    def turn_on(self) -> str:
        return "TV has been turned on"

    def turn_off(self) -> str:
        return "TV has been turned off"

    def change_channel(self, num) -> str:
        return f"Channel changed to channel number: {num}"

    def change_station(self, freq) -> str:
        return "Cannot change station in TV"

    def fly(self, direction) -> str:
        return "This TV cannot fly"


class RadioController(RemoteControl):
    device: str

    def turn_on(self) -> str:
        return "Radio has been turned on"

    def turn_off(self) -> str:
        return "Radio has been turned off"

    def change_channel(self, num) -> str:
        return "Cannot change channel in Radio"

    def change_station(self, freq) -> str:
        return f"Station changed to station with frequency: {freq}"

    def fly(self, direction) -> str:
        return "This Radio doesn't have any wings"


class DroneController(RemoteControl):
    device: str

    def turn_on(self) -> str:
        return "Drone has been turned on"

    def turn_off(self) -> str:
        return "Drone has been turned off"

    def change_channel(self, num) -> str:
        return "Cannot change channel in drone"

    def change_station(self, freq) -> str:
        return f"Cannot change station in drone"

    def fly(self, direction) -> str:
        return f"Flying: {direction}"
    
    
class Device(ABC):
    controller: RemoteControl
    
    def __init__(self, controller: RemoteControl) -> None:
        self.controller = controller
        
    @abstractmethod
    def take_action(self) -> str:
        pass
    
    
class TV(Device):
    controller: RemoteControl
    
    def take_action(self) -> str:
        to = self.controller.turn_on()
        cc = self.controller.change_channel(8)
        tf = self.controller.turn_off()
        return f"{to}\n{cc}\n{tf}"
    
    
class Radio(Device):
    controller: RemoteControl
    
    def take_action(self) -> str:
        to = self.controller.turn_on()
        cs = self.controller.change_station(67.8)
        tf = self.controller.turn_off()
        fd = self.controller.fly("up")
        return f"{to}\n{cs}\n{tf}\n{fd}"
    
    
class Drone(Device):
    controller: RemoteControl
    
    def take_action(self) -> str:
        to = self.controller.turn_on()
        fd = self.controller.fly("east")
        tf = self.controller.turn_off()
        return f"{to}\n{fd}\n{tf}"
    
    
tv_c = TVController("Panasonic")
radio_c = RadioController("RCD")
drone_c = DroneController("Blink")

tv = TV(tv_c)
radio = Radio(radio_c)
drone = Drone(drone_c)

print()
print(tv.take_action())
print()
print(radio.take_action())
print()
print(drone.take_action())


# ---------------------------------------------------------------------------


class Shape(ABC):
    shape: str

    def __init__(self, shape: str):
        self.shape = shape

    @abstractmethod
    def render_svg(self) -> str:
        pass

    @abstractmethod
    def render_bmp(self) -> str:
        pass


class Circle(Shape):
    def render_svg(self) -> str:
        circle = ("  -----  "
                  " /     \\"
                  " |     | "
                  " \\    / "
                  "   ----  ")

    def render_bmp(self) -> str:
        circle = ("001111100"
                  "011111110"
                  "111111111"
                  "111111111"
                  "011111110"
                  "001111100")
        return circle


class Rectangle(Shape):
    def render_svg(self) -> str:
        rec = ("-----"
               "|    |"
               "-----")
        return rec

    def render_bmp(self) -> str:
        rec = ("0000000"
               "0111110"
               "0111110"
               "0000000")
        return rec


class ShapeRenderer(ABC):
    shapes: Shape

    def __init__(self, shapes: Shape) -> None:
        self.shapes = shapes

    @abstractmethod
    def render_circle(self):
        pass

    @abstractmethod
    def render_rectangle(self):
        pass


class BMPRenderer(ShapeRenderer):
    shape: Shape

    def render_circle(self):
        pass
