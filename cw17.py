from abc import ABC, abstractmethod


class PaymentProcessor(ABC):
    @abstractmethod
    def authorize_payment(self, amount: float):
        pass

    @abstractmethod
    def capture_payment(self, transaction_id: str):
        pass


class CreditCardPayment(PaymentProcessor):
    def authorize_payment(self, amount: float):
        print(f"Credit Card: Autoryzacja kwoty {amount} PLN... Sprawdzanie limitu i kodu CVV.")
        return "CC_AUTH_98765"

    def capture_payment(self, transaction_id: str):
        print(f"Credit Card: Pobieranie środków dla transakcji {transaction_id}. Gotowe!")


class PayPalPayment(PaymentProcessor):
    def authorize_payment(self, amount: float):
        print(f"PayPal: Przekierowanie do logowania... Autoryzacja {amount} PLN przez portfel elektroniczny.")
        return "PP_TXN_12345"

    def capture_payment(self, transaction_id: str):
        print(f"PayPal: Finalizacja płatności {transaction_id}. Środki przesłane na konto sprzedawcy.")


ccp = CreditCardPayment()
ccp.authorize_payment(1000)
ccp.capture_payment("165423165416546354568")
ppp = PayPalPayment()
ppp.authorize_payment(2500)
ppp.capture_payment("456654465564564163516")
