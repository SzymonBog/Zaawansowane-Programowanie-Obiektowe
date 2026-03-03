class Store:
    total_customers = 0

    def add_customer(self):
        self.total_customers += 1

    def get_total_customers(self):
        return self.total_customers


s = Store()
print(s.get_total_customers())
s.add_customer()
print(s.get_total_customers())
s.add_customer()
print(s.get_total_customers())
s.add_customer()
print(s.get_total_customers())
s.add_customer()
print(s.get_total_customers())
