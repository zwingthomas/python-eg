from enum import Enum, Flag, auto


class Color(Enum):
    RED: str = 'R'
    GREEN: str = 'G'
    BLUE: str = 'B'


print(Color('R'))  # outputs: Color.RED
print(Color.RED)  # outputs: Color.RED
print(repr(Color.RED))  # outputs: <Color.RED: 'R'>
print(Color.RED.name)  # outputs: RED
print(Color.RED.value)  # outputs: R


def create_car(color: Color) -> None:
    match color:
        case Color.RED:
            print("A red car was created.")
        case Color.BLUE:
            print("A blue car was created.")
        case Color.GREEN:
            print("A green car was created.")
        case _:
            raise ValueError("Color not in enum!")


create_car(Color.BLUE)  # outputs: A blue car was created.

"""
Notice we are using the powers of two. Notice also we are using Flag
Flag is a different kind of enum that allows you to COMBINE enums.
"""


class Color(Flag):
    RED: int = 1
    GREEN: int = 2
    BLUE: int = 4
    YELLOW: int = 8
    BLACK: int = 16


yellow_and_red = Color = Color.YELLOW | Color.RED
print(yellow_and_red)  # outputs: Color.RED|YELLOW

for color in yellow_and_red:
    print(color)
    # outputs:
    # Color.RED
    # Color.YELLOW

"""
You can perform membership tests
"""

cool_colors = Color = Color.RED | Color.YELLOW | Color.BLACK
my_car_color: Color = Color.BLACK

if my_car_color in cool_colors:
    print("You have a cool car!")  # outputs
else:
    print("Sorry, your car is not cool.")

"""
Because we used the powers of two our combinations are now unique. If 
we were to have a Color at 9 the combination would be equal to the 
color assigned to it instead of the combination.
"""

combination: Color = Color.RED | Color.YELLOW
print(combination.value)  # outputs: 9


"""
In order to avoid having to know every power of two, simply use auto().
This is especially helpful when you have a significant number of enums.
"""


class Color(Flag):
    RED: int = auto()
    GREEN: int = auto()
    BLUE: int = auto()
    YELLOW: int = auto()
    BLACK: int = auto()
    ALL: int = RED | GREEN | BLUE | YELLOW | BLACK


print(Color.RED.value)  # outputs: 1
print(Color.GREEN.value)  # outputs: 2
print(Color.BLUE.value)  # outputs: 4
print(Color.YELLOW.value)  # outputs: 8
print(Color.BLACK.value)  # outputs: 16
print(Color.ALL.value)  # outputs: 31
print(Color.RED in Color.ALL)  # outputs: True


class State(Enum):
    OFF: int = 0
    ON: int = 1


switch: State = State.OFF

match switch:
    case State.ON:
        print('The lamp is turned on.')
    case State.OFF:
        print('The lamp is turned off.')
    case _:
        raise ValueError("Quantum lamps are not allowed")
