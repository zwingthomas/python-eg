

from abc import ABC, abstractmethod
print(len("Thomas Zwinger"))  # Calculates the length of the string
print(len([1, 2, 3, 4]))  # Calculates the length of the array

"""
These are two seperate calculations. They map back to two different
methods. However we call them in the same way! This a great example of polymorphism. You can see this same behavior with operators and other
syntax that maps back to dunder methods.
"""

print(1 + 1)
print([1] + [1])
print("1" + "1")


class PaymentType(ABC):

    @abstractmethod
    def process_payment(self, amount: float) -> None:
        ...


class CreditCard(PaymentType):
    def process_payment(self, amount):
        print(f'Processing credit card payment of ${amount}')


class Cash(PaymentType):
    def process_payment(self, amount):
        print(f'Processing cash payment of ${amount}')


class IOU(PaymentType):
    def process_payment(self, amount):
        print(f'Processing no payment of ${amount}')


def checkout(payment_type: PaymentType, amount: float) -> None:
    if issubclass(payment_type, PaymentType):
        payment_type = payment_type()
        payment_type.process_payment(amount)
        return
    raise TypeError("You must pay with a type of payment, not something else.")


"""
Notice how we can pass types directly into checkout and use them. This
will work provided that type implements process_payment from the 
abstract class which we can confirm by checking if it is inheriting the
type PaymentType with issubclass.
"""

checkout(CreditCard, 100)
checkout(Cash, 50)
checkout(IOU, 10)
