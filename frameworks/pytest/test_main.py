# Acknowledgements____
# Tech with Tim
# Please Learn How To Write Tests in Python… • Pytest Tutorial
# https://www.youtube.com/watch?v=EgpLj86ZHFQ&ab_channel=TechWithTim

"""
The python test files are all named "test_{module-to-test}". They need
to be prefixed with "test_" because that's how Python finds them.

To run the tests, go to the directory of the python code and then
run the pytest file with "pytest test_main.py"

Importance of unit testing: a unit test is the smallest type of test
and it's typically testing one very small "unit" or part of code. This
way if you are getting an error you are able to lock down exactly 
what it is by knowing exactly where it comes up in the program. There
are a lot of other types of tests but these are the most closely 
related to just the code. There is even Test Driven Development where
you right the tests before you write the code.

You want to test the less obvious things. Test the different things
that would make a system fail: the edge cases. To ensure the program
works in all given scenarios.

# TODO: Implement these for Traxy
"""


from main import add, divide, get_weather
import pytest


def test_get_weather():
    # passes
    assert get_weather(21) == "hot"


# def test_get_weather():
#     # fails
#     assert get_weather(21) == "cold"


def test_add():
    assert add(2, 3) == 5, "2 + 3 should be 5"
    assert add(-1, 1) == 0, "-1 + 1 should be 0"
    assert add(0, 0) == 0, "0 + 0 should be 0"


def test_divide():
    with pytest.raises(ValueError, match="Cannot divide by zero"):
        divide(10, 0)
