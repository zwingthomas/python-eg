"""
Thinking about a GUI where there are buttons that you press in order
to kick off some business logic. Think of the many buttons you've 
pressed today. An issue if they were to directly kick off the logic is
a tight coupling between the GUI and the business logic. All the 
components in the GUI need to know exactly what to call in the business
logic and this leads to issues with usability and testing.

The command takes all of the inputs from every button and then packages
it into one thing being sent to the business logic. This allows for
multiple servers for the business logic, load balancers, etc.

Briefly
- A request is wrapped in an object that contains all request info
- The command object is passed to the correct handler
- Decoupling
- Efficiency, ordering, priority, etc.

For our example we are going to implement an ordering system at a 
restaurant and pass it on to some sort of processor for processing.
This will be very abstract. You could do a lot more here by playing
with priority and balancing processing across servers.

"""
from abc import ABC, abstractmethod


class Command(ABC):
    def __init__(self, command_id: int):
        self.command_id = command_id

    @abstractmethod
    def execute(self):
        ...


class OrderAddCommand(Command):
    def execute(self):
        print(f"Adding order with id {self.command_id}")


class OrderPayCommand(Command):
    def execute(self):
        print(f"Paying for order with id {self.command_id}")


class CommandProcessor:
    queue = []

    def add_to_queue(self, command: Command):
        self.queue.append(command)

    def process_commands(self):
        [item.execute() for item in self.queue]
        self.queue = []


if __name__ == "__main__":
    processor = CommandProcessor()
    processor.add_to_queue(OrderAddCommand(1))
    processor.add_to_queue(OrderAddCommand(2))
    processor.add_to_queue(OrderPayCommand(1))
    processor.add_to_queue(OrderPayCommand(2))

    print("Processing...")
    processor.process_commands()
