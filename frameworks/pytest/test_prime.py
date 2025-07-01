import pytest
from prime import is_prime


@pytest.mark.parametrize("num, expected", [
    (1, False),
    (2, True),
    (3, True),
    (4, False),
    (17, True),
    (18, False),
    (19, True),
    (25, False)
])
def test_is_prime(num, expected):
    """ Parameterization saves us from a lot of typing """
    assert is_prime(num) == expected
