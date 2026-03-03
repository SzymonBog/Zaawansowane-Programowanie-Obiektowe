class MathOperations:
    @staticmethod
    def add(a: float, b: float):
        res = a + b
        return res

    @staticmethod
    def multiply(a: float, b: float):
        res = a * b
        return res

    @classmethod
    def identity_matrix(cls, size: int):
        ar = []
        for i in range(size):
            arr = []
            for j in range(size):
                if j == i:
                    arr.append(1)
                else:
                    arr.append(0)
            ar.append(arr)
        return ar


mo = MathOperations()
im = mo.identity_matrix(5)
print(im, MathOperations.add(1, 3), MathOperations.multiply(5, 6))
