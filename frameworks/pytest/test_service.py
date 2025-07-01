import pytest
from service import UserService, APIClient

"""
Here we mock an entire class!!
"""


def test_get_username_with_mock(mocker):
    # Create a mock API client
    mock_api_client = mocker.Mock(spec=APIClient)

    # Mock get_user_data to return a fake user
    mock_api_client.get_user_data.return_value = {"id": 1, "name": "Letice"}

    # Inject mock API client
    service = UserService(mock_api_client)

    # Call method that depends on the mock
    # Not mocking that method, but it **depends** on the mock
    result = service.get_username(1)

    # Assertions
    assert result == "LETICE"
    mock_api_client.get_user_data.assert_called_once_with(1)
