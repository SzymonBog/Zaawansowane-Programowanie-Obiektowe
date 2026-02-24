class Employee:
    def __init__(self, first: str, last: str, sal: float):
        self.first_name = first
        self.last_name = last
        self.salary = sal

    def get_full_name(self):
        return self.first_name + " " + self.last_name


class Manager(Employee):
    department = ""

    def __init__(self, first: str, last: str, sal: float, dep: str):
        super().__init__(first, last, sal)
        self.department = dep

    def get_department_info(self):
        return self.department


e1 = Employee("Mike", "Shmidt", 50)
print(e1.get_full_name())

m1 = Manager("Kelly", "Wright", 250, "Computer")
print(m1.get_full_name() + " " + m1.get_department_info())
