class Person:
    def introduce(self):
        return "I am a person"


class Worker(Person):
    def introduce(self):
        return "I am a worker"


class Student(Person):
    def introduce(self):
        return "I am a student"


class WorkingStudent(Worker, Student):
    pass


p = Person()
w = Worker()
s = Student()
ws = WorkingStudent()
print(f"{p.introduce()}\n{w.introduce()}\n{s.introduce()}\n{ws.introduce()}")
