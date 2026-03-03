class IDGenerator:
    current_id = 0

    @classmethod
    def generate_id(cls):
        cls.current_id = cls.current_id + 1
        return cls.current_id

    def __init__(self):
        self.id = self.current_id  # IDGenerator.generate_id()

    def get_id(self):
        return self.id


id1 = IDGenerator()
id1.generate_id()
id2 = IDGenerator()
id2.generate_id()
id3 = IDGenerator()
id3.generate_id()
id4 = IDGenerator()
id4.generate_id()
print(id1.get_id())
print(id2.get_id())
print(id3.get_id())
print(id4.get_id())
