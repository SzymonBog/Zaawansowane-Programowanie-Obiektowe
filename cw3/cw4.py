from abc import ABC, abstractmethod
from typing import Self, Any


class Component(ABC):
    _parent: Self

    def __init__(self) -> None:
        self._parent = None

    @property
    def parent(self) -> Self:
        return self._parent

    @parent.setter
    def parent(self, parent: Self) -> None:
        self._parent = parent

    def get_parent(self) -> Self:
        return self._parent

    def add(self, component: Self) -> None:
        pass

    def remove(self, component: Self) -> None:
        pass

    #def go_to(self, directory) -> None:
    #    pass

    #def go_up(self) -> None:
    #    pass

    def move(self, object_to_move, target):
        pass


class Directory(Component):
    name: str
    path: str

    def __init__(self, name, path) -> None:
        super().__init__()
        self.name = name
        self.path = path
        self.children = []

    def add(self, component: Any) -> None:
        component.parent = self
        self.children.append(component)

    def remove(self, component: Any) -> None:
        component.parent = None
        self.children.remove(component)

    def move(self, object_to_move, target): # ?
        for child in self.children:
            if Directory == type(target):
                if object_to_move == None:
                    if Directory == type(object_to_move):
                        self.move_dir(target)
                    child.move(target)
                elif child == object_to_move:
                    if Directory == type(object_to_move):
                        self.move_dir(target)
                    child.move(target)
                    break

    def move_dir(self, target):
        self.parent = target
        self.path = target


class File(Component):
    name: str
    path: str

    def __init__(self, name, path) -> None:
        super().__init__()
        self.name = name
        self.path = path

    def move(self, target): # ?
        print(self.path, target)
        self.path = target
        print("Moved")


d1 = Directory("root", "")
d2 = Directory("dir1", d1)
d3 = Directory("dir3", d1)
f1 = File("file1", d3)
d1.add(d2)
d3.add(f1)
d1.add(d3)

print(f1.path)
d3.move(None, d2)
print(f1.path)
