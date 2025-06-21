import pytest
from http import HTTPStatus
from api_clients_and_models.models.login_models import LoginResponseModel
from user_accounts_resources.invalid_data.invalid_user_auth_data import invalid_login_data
from utils.custom_asserts import assert_response_schema


@pytest.mark.prod_safe
def test_correct_login(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    response = auth_client.login_user_request(user=user)

    result = assert_response_schema(LoginResponseModel, response, expected_status=HTTPStatus.OK)
    assert result.is_valid(), f"Response schema validation failed: {''.join(result.errors)}"


def test_login_with_newly_created_user(auth_client, register_new_user):
    user = register_new_user
    response = auth_client.login_user_request(user=user)

    result = assert_response_schema(LoginResponseModel, response, expected_status=HTTPStatus.OK)
    assert result.is_valid(), f"Response schema validation failed: {''.join(result.errors)}"


@pytest.mark.parametrize("user_data", invalid_login_data.values(), ids=invalid_login_data.keys())
def test_incorrect_login(make_user, auth_client, user_data):

    response = auth_client.login_user_request(username=user_data["username"], password=user_data["password"])

    assert response.status_code == HTTPStatus.UNAUTHORIZED, f"Expected 401 Unauthorized, got {response.status_code}"


def test_login_with_incorrect_password(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    response = auth_client.login_user_request(username=user.username, password=f"{user.password}123")

    assert response.status_code == HTTPStatus.UNAUTHORIZED, f"Expected 401 Unauthorized, got {response.status_code}"
    assert response.json().get("message") == "Invalid credentials", "Expected 'Invalid credentials' message in response"

