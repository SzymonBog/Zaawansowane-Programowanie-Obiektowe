import random
from abc import ABC, abstractmethod
from typing import Any


class Observable(ABC):
    _observers: set

    def __init__(self) -> None:
        self._observers = set()

    def add_observer(self, observer: Any) -> None:
        self._observers.add(observer)

    def delete_observer(self, observer: Any) -> None:
        self._observers.remove(observer)

    def notify(self, *args: list, **kwargs: dict) -> None:
        for observer in self._observers:
            observer.notify(stock=self, *args, **kwargs)


class Observer(ABC):
    def __init__(self, observable: Observable):
        observable.add_observer(self)

    @abstractmethod
    def notify(self, *args: list, **kwargs: dict) -> None:
        pass


class Stock(Observable):
    currency: str
    base_value: float
    current_value: float

    def __init__(self, currency: str, base_value: float) -> None:
        super().__init__()
        self.currency = currency
        self.base_value = base_value
        self.current_value = base_value

    def change_value_times(self, mult: float) -> None:
        self.current_value *= mult
        self.notify(self.base_value, self.current_value)


class Buyer(Observer):
    def notify(self, *args: list, **kwargs: dict):
        print(args)
        stocks = kwargs["stock"]
        if args[1] > args[0]:
            print(f"Sell {stocks}")
        else:
            print(f"Buy {stocks}")


euro = Stock("euro", 4.2)

buyer_1 = Buyer(euro)
buyer_2 = Buyer(euro)

for _ in range(20):
    r = random.randrange(-3, 5)
    mult = 1

    if r < 0:
        mult = 1 / random.randrange(2, 3)
    elif r == 1:
        mult = 1
    else:
        mult = 1 + 1 / random.randrange(2, 6)

    euro.change_value_times(mult)


# ---------------------------------------------------------------------


class ObservableServer(ABC):
    _observers: set

    def __init__(self) -> None:
        self._observers = set()

    def add_observer(self, observer: Any) -> None:
        self._observers.add(observer)

    def delete_observer(self, observer: Any) -> None:
        self._observers.remove(observer)

    def activate(self, *args: list, **kwargs: dict) -> None:
        for observer in self._observers:
            observer.activate(system=self, *args, **kwargs)


class OutsideObserver(ABC):
    def __init__(self, observable: ObservableServer):
        observable.add_observer(self)

    @abstractmethod
    def activate(self, *args: list, **kwargs: dict) -> None:
        pass


class Server(ObservableServer):
    name: str
    working: int

    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.working = 1

    def work(self) -> None:
        error = random.randint(0, 1)
        if error == 1:
            self.deactivate()
        else:
            print("Working")

    def deactivate(self) -> None:
        if self.working:
            self.working = 0
            self.activate([self.working])
        else:
            self.working = 1
            self.activate([self.working])


class Email(OutsideObserver):
    def activate(self, *args: list, **kwargs: dict) -> None:
        system = kwargs["system"]

        if system == 0:
            print("Emails activated")
        else:
            print("Emails deactivated")


class SMS(OutsideObserver):
    def activate(self, *args: list, **kwargs: dict) -> None:
        system = kwargs["system"]

        if system == 0:
            print("SMS activated")
        else:
            print("SMS deactivated")


class Logs(OutsideObserver):
    def activate(self, *args: list, **kwargs: dict) -> None:
        system = kwargs["system"]

        if system == 0:
            print("Logs activated")
        else:
            print("Logs deactivated")


server = Server("bob")
gmail = Email(server)
orange = SMS(server)
logs = Logs(server)
server.add_observer(gmail)
server.add_observer(orange)
server.add_observer(logs)

for _ in range(20):
    server.work()


# -----------------------------------------------------------------------


class ObservableDetector(ABC):
    _observers: set

    def __init__(self) -> None:
        self._observers = set()

    def add_observer(self, observer: Any) -> None:
        self._observers.add(observer)

    def delete_observer(self, observer: Any) -> None:
        self._observers.remove(observer)

    def alert(self, *args: list, **kwargs: dict) -> None:
        for observer in self._observers:
            observer.activate(alert=self, *args, **kwargs)


class BaseObserver(ABC):
    def __init__(self, observable: ObservableServer):
        observable.add_observer(self)

    @abstractmethod
    def activate(self, *args: list, **kwargs: dict) -> None:
        pass


class MovementDetector(ObservableDetector):
    number: int
    
    def __init__(self, number: int) -> None:
        super().__init__()
        self.number = number

    def watch(self) -> None:
        see = random.randint(0, 1)
        if see == 1:
            self.alert(["Movement detected"])
