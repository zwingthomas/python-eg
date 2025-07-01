"""
Used when we need to apply a certain functionality to a component in
our code. Generally this component will be a tree-shape. Consider a 
computer. A computer has Memory, HDD, and Processor. These can be
further broken down into Memory -> a.RAM b.ROM, giving us a tree shape.
Now if we were to want to get the price we would be able to take the
price from these trees and sum up the price of the RAM and ROM as the
price of the Memory and the price of the Memory, the HDD, and the 
Processor as the total price.

Briefly,
- Compose objects into tree structures
- Works when the core functionality can be represented as a tree
- Manipulate many objects as a single one

We are going to implement what we've talked about as a theoretical
example.
"""


class Equipment:
    """Acts as the tree leaves"""

    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price


class Composite:
    """Acts as the tree nodes"""

    def __init__(self, name: str):
        self.name = name
        self.items = []

    def add(self, equipment: Equipment):
        self.items.append(equipment)
        return self

    @property
    def price(self):
        return sum(x.price for x in self.items)

    @price.setter
    def price(self, value):
        self.price = value


if __name__ == "__main__":
    computer = Composite("PC")
    processor = Equipment("Processor", 1000)
    hard_drive = Equipment("Hard drive", 250)
    memory = Composite("Memory")
    rom = Equipment("Read only memory", 100)
    ram = Equipment("Random access memory", 75)
    # Notice it doesn't matter what order we add the nodes
    computer.add(processor).add(hard_drive).add(memory)
    memory.add(rom).add(ram)
    print(f"{rom.price} + {ram.price} = {memory.price}")
    print(f"{processor.price} + {hard_drive.price} + {memory.price} = {computer.price}")
