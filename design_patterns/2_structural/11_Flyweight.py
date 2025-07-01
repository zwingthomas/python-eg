"""
All about reducing the load. In a memory system it reduces the amount
of things you have to store in memory. In a processing system it 
reduces the amount of processing you need to do for the same outcome.

Imagine you had a bunch of avatars in a game. You may want to store
every soldier in memory when it is visible. However, that will fill
up memory quite quickly. Instead you could have a factory for the
avatars and use these in memory when you require it. All replicas
stored in one place. Some of the information, like the state, is 
unique. However, much of the data, like the sprites for these avatars,
can and should be shared. This allows for memory and processing to 
have a lower footprint. 

Briefly,
- Works well when you have lots of similar objects
- Reduces the memory footprint
- Very efficiency focused

"""
from abc import ABC, abstractmethod
import random


class Sprite(ABC):
    @abstractmethod
    def draw(self):
        ...

    @abstractmethod
    def move(self, x: int, y: int):
        ...


class FighterRank:
    private = 0
    sergeant = 1
    major = 2


class Fighter(Sprite):
    def __init__(self, rank: FighterRank):
        self.rank = rank

    def draw(self):
        print(f"Drawing fighter: {self}")

    def move(self, x: int, y: int):
        print(f"Moving fighter: {self} to position {x=} {y=}")


class FighterFactory:
    def __init__(self):
        self.fighters = [None, None, None]

    def get_fighter(self, rank: FighterRank):
        try:
            f = self.fighters[rank]
        except:
            f = None
        if not f:
            f = Fighter(rank)
            self.fighters[rank] = f
        return f


class Army:
    army = []

    def __init__(self):
        self.fighter_factory = FighterFactory()

    # When we spawn fighters they are all coming from that same factory
    # which is an array of size three. If they were larger assets this
    # would be very critical for performance.
    def spawn_fighter(self, rank: FighterRank):
        self.army.append(self.fighter_factory.get_fighter(rank))

    def draw_army(self):
        for fighter in self.army:
            if fighter.rank == FighterRank.major:
                print("M", end="")
            if fighter.rank == FighterRank.sergeant:
                print("S", end="")
            else:
                print("P", end="")


if __name__ == "__main__":
    army_size = 1000000
    army = Army()

    for i in range(army_size):
        r = random.randrange(2)
        army.spawn_fighter(r)

    army.draw_army()
