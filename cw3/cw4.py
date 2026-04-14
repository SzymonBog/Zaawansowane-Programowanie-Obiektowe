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

    def move(self, target):
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

    def remove(self, component: Any) -> None: # redo
        component.parent = None
        component.path = None

        for child in self.children:
            child.remove(component)

    def move(self, target): # ?
        if Directory == type(target):
            self.move_dir(target)
            """
            for child in self.children:
                #print(child.name, child.path)
                if type(child) == Directory:
                    child.move_dir(target)
                else:
                    child.move(target)
            """

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
        self.parent = path

    def move(self, target): # ?
        print(self.path, target)
        if Directory == type(target):
            self.path = target
            self.parent = target  # !
            print("Moved")

    def remove(self, component: Any) -> None:
        self.path = None
        self.parent = None
        print("removed")


d0 = Directory("root", "")
d1 = Directory("dir1", d0)
d2 = Directory("dir2", d0)
f1 = File("file1", d1)
d3 = Directory("dir3", d2)
d4 = Directory("dir4", d3)
f2 = File("file2", d4)
d0.add(d1)
d0.add(d2)
d1.add(f1)
d2.add(d3)
d3.add(d4)
d4.add(f2)

for i in [d0, d1, d2, f1, d3, d4, f2]:
    if i.parent is not None:
        print(i.name, i.path, i.parent.name)
    else:
        print(i.name, i.path)

d3.move(d1)

for i in [d0, d1, d2, f1, d3, d4, f2]:
    if i.parent is not None:
        print(i.name, i.path, i.parent.name)
    else:
        print(i.name, i.path)

d3.remove(d4)

for i in [d0, d1, d2, f1, d3, d4, f2]:
    if i.parent is not None:
        print(i.name, i.path, i.parent.name)
    else:
        print(i.name, i.path)


# -------------------------------------------


class UserComponent(ABC):
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


class Group(UserComponent):
    name: str
    permissions: str

    def __init__(self, name, permissions) -> None:
        super().__init__()
        self.name = name
        self.permissions = permissions
        self.guests = []

    def add(self, component: Any) -> None:
        if type(component) == Group:
            for g in component.guests:
                g.give_permissions(self.permissions)
            # component.parent = self
            # self.guests.append(component)
        else:
            component.parent = self
            self.guests.append(component)
            component.permissions = self.permissions

    def remove(self, component: Any) -> None: # redo
        component.parent = None
        component.permissions = None

        #for child in self.guests:
        #    child.remove(component)


class User(UserComponent):
    name: str
    permissions: str

    def __init__(self, name, permissions) -> None:
        super().__init__()
        self.name = name
        self.permissions = permissions
        self.parent = permissions

    def give_permissions(self, permissions: Any) -> None:
        self.permissions = permissions

    def remove(self, component: Any) -> None:
        self.permissions = None
        self.parent = None
        print("removed")


u1 = User("u1", None)
u2 = User("u2", None)
u3 = User("u3", None)
u4 = User("u4", None)
u5 = User("u5", None)
u6 = User("u6", None)
g1 = Group("g1", ["select"])
g2 = Group("g2", ["select, create"])
g3 = Group("g3", ["select, create, delete"])

g1.add(u1)
g1.add(u2)
g2.add(u3)
g2.add(u4)
g3.add(u5)
g3.add(u6)
g3.remove(u6)

g1.add(g2)

u6.give_permissions(g2.permissions)

for g in [g1, g2, g3]:
    for u in g.guests:
        print(u.name, u.permissions)


# ---------------------------------------------------------


class ReportComponent(ABC):
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


class ReportGroup(ReportComponent):
    name: str
    values: dir

    def __init__(self, name, values) -> None:
        super().__init__()
        self.name = name
        self.values = values
        self.attached_reports = []

    def add(self, component: Any) -> None:
        component.parent = self
        self.attached_reports.append(component)

    def remove(self, component: Any) -> None: # redo
        component.parent = None
        component.attached_reports = None

    def __str__(self):
        ar = ""
        for i in self.attached_reports:
            ar += str(i)

        return f"{self.name} {self.values} {ar}"


rg1 = ReportGroup("r1", {"1":123, "2":456, "3":789})
rg2 = ReportGroup("r2", {"1":123*2, "2":456/1.5, "3":789/3})
rg3 = ReportGroup("r3", {"1":4516, "2":789, "3":789})

rg2.add(rg3)
rg1.add(rg2)
print(rg1)
