import random


class OldSys:
    def __init__(self, year: int):
        self.year = year

    def pip(self):
        print("Pip pip pip")

    def print_old(self, sentence):
        print(f"Hi, {sentence}")


class NewSys:
    def __init__(self, year: int):
        self.year = year

    def base(self):
        print("BAZA WIRUSÓW AVAST ZOSTAŁĄ ZAKTUALIZOWANA")

    def print_new(self, sentence):
        print(f"Hello, {sentence}")


class OldSysAdapter:
    def __init__(self, new_sys: NewSys) -> None:
        self.new_sys = new_sys

    def pip(self):
        print("Pip pip pip")

    def print_new(self, sentence):
        self.new_sys.print_new(sentence)


old = OldSys(1975)
new = NewSys(2020)
old.print_old("I am old")
old.pip()
new.print_new("I'm new")
new.base()
costumed_old = OldSysAdapter(new)
costumed_old.print_new("I'm old")
costumed_old.pip()


# -----------------------------------------

class FahrenheitSensor:
    def __init__(self):
        self.temp = 0

    def read_temperature(self):
        self.temp = random.randint(0, 300)
        return self.temp


class TemperatureAdapter:
    def __init__(self, fahr: FahrenheitSensor):
        self.temp = 0
        self.fahr = fahr

    def read_temperature(self):
        t = self.fahr.read_temperature()
        self.temp = (t - 32) / 1.8
        return f"{self.temp} C, {t} F"


fahr = FahrenheitSensor()
print(fahr.read_temperature())

ta = TemperatureAdapter(fahr)
print(ta.read_temperature())


# --------------------------------------


class PayPalPay:
    def __init__(self, wallet: str, money: float):
        self.wallet = wallet
        self.money = money

    def pay(self, amount: float, recipient: str):
        self.money = self.money - amount
        print(f"Paypal transaction finalized. {recipient} got {amount}$")


class Stripe:
    def __init__(self, wallet: str, money: float):
        self.wallet = wallet
        self.money = money

    def pay_amount(self, amount: float, reciever: str):
        self.money = self.money - amount
        print(f"Paypal transaction finalized. Transferred {amount} to {reciever}")


class PaymentAdapter:
    def __init__(self, wallet: str, money: float, paypal: PayPalPay, stripe: Stripe):
        self.wallet = wallet
        self.money = money
        self.paypal = paypal
        self.stripe = stripe

    def transfer_money(self, amount: float, person: str):
        if amount <= 1000:
            self.paypal.pay(amount, person)
        else:
            self.stripe.pay_amount(amount, person)


ppp = PayPalPay("shfg654gfh6s34hsf46ghsf52ght4", 100000)
ppp.pay(100, "Mike")

s = Stripe("654tfrhtfh4565412hdtbdg132465", 99999)
s.pay_amount(465, "Lauren")

pa = PaymentAdapter("e564rg46g9586g5r4e869r5ed4g584r6eg", 9845649, ppp, s)
pa.transfer_money(666, "Jane")
pa.transfer_money(6420, "Kate")
