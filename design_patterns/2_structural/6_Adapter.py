"""
The adapter is very easy to understand, it simply converts the
interface of a class into another interface that the client expects.

Such as if we wanted to work with a 3rd party library, but our client
was incompatible with it. We would need an adapter to link the two.

Briefly,
- Converts data or calls from one form into the other.

Essentially:
Client
<->
Target Call()
<->
Adapter [call()->specificCall()]
<->
Adaptee specificCall()


"""

from dataclasses import dataclass


@dataclass
class DisplayDataType:
    """Third-party functionality for our purposes"""
    index: float
    data: str


class DisplayData:
    """Third-party functionality for our purposes"""

    def __init__(self, display_data: DisplayDataType):
        self.display_data = display_data

    def show_data(self):
        print(
            "3rd party functionality: " +
            f"{self.display_data.index} - {self.display_data.data}"
        )


@dataclass
class DatabaseDataType:
    """Our home grown functionality for our purposes"""
    position: int
    amount: int


class StoreDatabaseData:
    """Our home grown functionality for our purposes"""

    def __init__(self, database_data: DatabaseDataType):
        self.database_data = database_data

    def store_data(self, data):
        print("Database date stored: " +
              f"{self.database_data.position} - {self.database_data.amount}")


class DisplayDataAdapter(StoreDatabaseData, DisplayData):
    """
        The adapter

        Should inherit from both what it is adapting and the information
        that must be augmented. In this case we are overriding
        store_data from StoreDatabaseData that uses the DatabaseDataType
        and we are passing it into DisplayData, the 3rd party 
        functionality which requires a DisplayDataType
    """

    def __init__(self, data):
        self.data = data

    def store_data(self):
        print("Call out code but use 3rd party code")
        for item in self.data:
            ddt = DisplayDataType(float(item.position), str(item.amount))
            self.display_data = ddt
            self.show_data()


def generate_data():
    data = list()
    data.append(DatabaseDataType(2, 2))
    data.append(DatabaseDataType(3, 7))
    data.append(DatabaseDataType(9, 1))
    return data


if __name__ == "__main__":
    adapter = DisplayDataAdapter(generate_data())
    adapter.store_data()
