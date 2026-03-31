from abc import ABC, abstractmethod
from typing import Any
from time import time




class UserClass(ABC):
    @abstractmethod
    def important_method(self) -> str:
        pass


class User(UserClass):
    def __init__(self, login, password, role):
        self.login = login
        self.password = password
        self.role = role

    def important_method(self) -> str:
        return "You have access to: "


class Decorator(ABC):
    def __init__(self, obj: Any) -> None:
        self.object = obj

    @abstractmethod
    def important_method(self) -> str:
        pass


class ClassDecorator(Decorator):
    def important_method(self) -> str:
        if self.object.role == "Admin":
            return f"{self.object.important_method()} read/print, create, update, delete, alter commands"
        elif self.object.role == "Moderator":
            return f"{self.object.important_method()} read/print, create, update commands"
        elif self.object.role == "Guest":
            return f"{self.object.important_method()} read/print commands"


admin = User("admin", "123", "Admin")
mod = User("mod", "123", "Moderator")
guest = User("guest", "123", "Guest")

adminDec = ClassDecorator(admin)
modDec = ClassDecorator(mod)
guestDec = ClassDecorator(guest)

print(adminDec.important_method())
print(modDec.important_method())
print(guestDec.important_method())

print(admin.important_method())
print(mod.important_method())
print(guest.important_method())


# -------------------------------------------


class FormClass(ABC):
    @abstractmethod
    def set_form(self, name, answer1, answer2, answer3, answer4):
        pass


class Form(FormClass):
    def __init__(self, name, answer1, answer2, answer3, answer4):
        self.name = name
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4

    def set_form(self, name, answer1, answer2, answer3, answer4):
        self.name = name
        self.answer1 = answer1
        self.answer2 = answer2
        self.answer3 = answer3
        self.answer4 = answer4


class Decorator2(ABC):
    def __init__(self, obj: Any) -> None:
        self.object = obj
        self.check_answers()

    @abstractmethod
    def check_answers(self) -> str:
        pass


class FormDecorator(Decorator2):
    def check_answers(self) -> str:
        errors = 0
        if type(self.object.name) != str:
            errors += 1
        if type(self.object.answer1) != str:
            errors += 1
        if type(self.object.answer2) != str:
            errors += 1
        if type(self.object.answer3) != str:
            errors += 1
        if type(self.object.answer4) != str:
            errors += 1
        if errors > 0:
            raise ValueError("Expected string")


form = Form("Jakub", "a", "b", "1", "d")
formD = FormDecorator(form)
formD.check_answers()
# form.set_form("Mariusz", "sad", "g", 1, "o")
formD2 = FormDecorator(form)
formD2.check_answers()


# --------------------------------------------


def timeit(fn: callable) -> callable:
    def wrappper(*args: list) -> str:
        start = time()
        result = fn(*args)
        stop = time()
        print(stop - start)
        return result
    return wrappper


class DatabaseClass:
    def __init__(self, dataset1, dataset2, dataset3, dataset4, dataset5):
        self.dataset1 = dataset1
        self.dataset2 = dataset2
        self.dataset3 = dataset3
        self.dataset4 = dataset4
        self.dataset5 = dataset5

    @timeit
    def add(self, dataset_number, value):
        match dataset_number:
            case 1:
                self.dataset1.append(value)
            case 2:
                self.dataset2.append(value)
            case 3:
                self.dataset3.append(value)
            case 4:
                self.dataset4.append(value)
            case 5:
                self.dataset5.append(value)
            case _:
                return "Dataset not found"
        return "Value added"

    @timeit
    def delete(self, dataset_number, value):
        match dataset_number:
            case 1:
                self.dataset1.remove(value)
            case 2:
                self.dataset2.remove(value)
            case 3:
                self.dataset3.remove(value)
            case 4:
                self.dataset4.remove(value)
            case 5:
                self.dataset5.remove(value)
            case _:
                return "Dataset not found"
        return "Value removed"


ds1 = [1, 6, 3, 7]
ds2 = [1, 7, 9, 4]
ds3 = [5, 8, 3, 4]
ds4 = [4, 2, 9, 3]
ds5 = [1, 8, 3, 5]
dbc = DatabaseClass(ds1, ds2, ds3, ds4, ds5)
print(dbc.add(1, 9))
print(dbc.delete(2, 4))
print(dbc.dataset1)
