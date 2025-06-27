"""
This is a factory that creates factories.

Let's say we had a bunch of data sources. All have different types
for their database, for their user input, for information from the
network. The display does not really care where it got the data
provided it can get the data from somewhere and it is the data it
wants. Thus, we create a DataSourceFactory that instantiates a 
DataFactory that implements the Database. It also makes a NetworkFactory
that can get us access to whatever it in the network.

Key points:
- Provides a way to access functionality without caring about 
    implementation
- One level of abstraction over the factory pattern
- Separation of concerns
- Allows for testability


We are going to create an abstract factory where you can dine at a
restaurant. You can get some American food, French food, etc. The
factory will create the restaurants, the restaurants are themselves
factories. The user will not really care what food they receive in
this case.

"""

from abc import ABC, abstractmethod


class FoodType:
    french = 1
    american = 2


class Restaurant(ABC):
    @abstractmethod
    def make_food(self):
        ...

    @abstractmethod
    def make_drink(self):
        ...


class FrenchRestaurant(Restaurant):
    """This is a factory"""

    def make_food(self):
        print("Cigarettes")

    def make_drink(self):
        print("Fancy coffee in small cup")


class AmericanRestaurant(Restaurant):
    """This is another factory"""

    def make_food(self):
        print("A plate of bacon")

    def make_drink(self):
        print("Diet Coke")


class RestaurantFactory:
    """This is a factory that makes the factories: an abstract factory"""
    @staticmethod
    def suggest_restaurant(r_type: FoodType):
        if r_type == FoodType.french:
            return FrenchRestaurant()
        if r_type == FoodType.american:
            return AmericanRestaurant()

# client function


def dine_at(restaurant: Restaurant):
    print("For dinner we are having: ")
    restaurant.make_drink()
    restaurant.make_food()


if __name__ == "__main__":
    # The Restaurant Factory suggests which factory to use based
    # on a type given to it.
    suggestion1 = RestaurantFactory.suggest_restaurant(FoodType.french)
    suggestion2 = RestaurantFactory.suggest_restaurant(FoodType.american)

    print(suggestion1)
    dine_at(suggestion1)
    print()
    print(suggestion2)
    dine_at(suggestion2)
