from typing import Self


class Iterator:
    n: int
    sub: int
    limit: int

    def __init__(self, limit: int) -> None:
        self.n = limit
        self.limit = 0
        self.sub = 1

    def __iter__(self) -> Self:
        return self

    def __next__(self) -> int:
        if self.n - 1 >= self.limit:
            self.n -= self.sub
            # self.sub -= 2
            return self.n

        raise StopIteration


iterator = Iterator(20)

for i in iterator:
    print(i)


# -------------------------------------------------------------------------


class OrderIterator:
    finished_orders: list
    orders_in_progres: list
    new_orders: list
    state: str
    n: int
    limit: int

    def __init__(self, orders: dict) -> None:
        self.n = 0
        self.state = "new"
        self.new_orders = []
        self.orders_in_progres = []
        self.finished_orders = []

        for i in orders:
            if orders[i] == "new":
                self.new_orders.append(i)
            elif orders[i] == "in progres":
                self.orders_in_progres.append(i)
            elif orders[i] == "done":
                self.finished_orders.append(i)

    def __iter__(self) -> Self:
        return self

    def set_state(self, state: str):
        self.state = state
        self.n = 0

        if self.state == "new":
            self.limit = len(self.new_orders)
        elif self.state == "in progres":
            self.limit = len(self.orders_in_progres)
        elif self.state == "done":
            self.limit = len(self.finished_orders)

    def __next__(self):
        if self.n < self.limit:
            if self.state == "new":
                r = self.new_orders[self.n]
            elif self.state == "in progres":
                r = self.orders_in_progres[self.n]
            elif self.state == "done":
                r = self.finished_orders[self.n]
            self.n += 1
            return r

        raise StopIteration


oi = OrderIterator({"bm": "in progres", "ch": "new", "bm2de": "done", "bm1": "in progres", "bgdsf": "done"})
oi.set_state("new")
for i in oi:
    print(i)

oi.set_state("in progres")
for i in oi:
    print(i)

oi.set_state("done")
for i in oi:
    print(i)
