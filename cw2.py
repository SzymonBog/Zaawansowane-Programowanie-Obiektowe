from collections import namedtuple

Transaction = namedtuple("Transaction", ["transaction_id", "amount", "currency"])


class BankAccount:

    def __init__(self, bal):
        self.balance = bal

    def apply_transaction(self, transaction: Transaction):
        self.balance = self.balance + transaction.amount

    def get_balance(self):
        return self.balance


account = BankAccount(10000)
print(account.get_balance())
t1 = Transaction("1648326", 5000, "USD")
t2 = Transaction("1648327", -500, "USD")
account.apply_transaction(t1)
print(account.get_balance())
account.apply_transaction(t2)
print(account.get_balance())
