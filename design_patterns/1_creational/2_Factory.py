"""
Sometimes your requirements change. This design pattern creates a 
seperation between the user of the object and the creator of the 
object. This allows for more extensible code that is able to change
dynamically. This also allows for seperation of concerns between the
object, the creation of the object, and how to use it. It does this
through encapsulation and polymorphism.

Briefly,
- Design logic is hidden from the client
- Many subclass types, only one instance is required
- Creation is removed from the client
- Useful for frequent code changes: The seperation is done so that
    you can add or subtract types and the code will not change too 
    much.

Think about a database factory. All the databases connecting (e.g. 
SQLite, MySQL, SQL Server) will have different ways of connecting,
this can be masked by a database factory that generates their 
connectors for them depending on the type of database.

- Interface or abstract class that defines the common functionality
- Interface implementations
- Factory class that instantiates the right implementation

We are going to create a currency factory that gives you the currency
for a given country type.
"""

from abc import ABC, abstractmethod


class Country:
    ...


class USA(Country):
    ...


class Brazil(Country):
    ...


class Japan(Country):
    ...


class CurrencyFactory(ABC):
    @abstractmethod
    def currency_factory(self, country) -> str:
        ...


class FiatCurrencyFactory(CurrencyFactory):
    """This is one factory"""

    def currency_factory(self, country) -> str:
        if country is USA:
            return "Dollar"
        elif country is Brazil:
            return "Real"
        else:
            return "Yen"


class VirtualCurrencyFactory(CurrencyFactory):
    """This is another factory"""

    def currency_factory(self, country):
        if country is USA:
            return "Bitcoin"
        if country is Brazil:
            return "Ripple"
        else:
            return "Ethereum"


if __name__ == "__main__":
    f1 = FiatCurrencyFactory()
    f2 = VirtualCurrencyFactory()

    for country in [USA, Brazil, Japan]:
        print(country)
        print(f1.currency_factory(country))
        print(f2.currency_factory(country))
