"""
A lot of time with unit tests there is a part of your code that relies
on an aspect that isn't within this set of code in order to run. You
would not want to error on this because it would show an error up or
down stream instead of showing an error for just your isolated area
which is what a unit test is meant to do.

TODO: What is an upstream dependency? Downstream?
"""

import pytest
from mocks import get_weather


def test_get_weather(mocker):
    # Mock requests.get
    mock_get = mocker.patch("mocks.requests.get")

    # Set return values
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = {"tempurature": 25,
                                               "condition": "Sunny"}

    # Call function
    result = get_weather("Dubai")

    # Assertions
    assert result == {"tempurature": 25, "condition": "Sunny"}
    mock_get.assert_called_once_with("https://api.weather.com/v1/Dubai")
