import pytest
from http import HTTPStatus

from api_client.validation_models.signup_models import RegistrationResponse
from user_resources.invalid_data.invalid_user_login_data import invalid_signup_data
from utils.custom_asserts import assert_response_schema


def test_correct_signup(make_user, auth_client, save_registered_user):
    user = make_user()
    response = auth_client.register_user_request(user=user)

    result = assert_response_schema(RegistrationResponse, response, expected_status=HTTPStatus.OK)
    assert result.is_valid(), f"Response schema validation failed: {''.join(result.errors)}"
    assert result.data.username == user.username, f"Expected username {user.username}, got {result.data.username}"
    save_registered_user(user)


@pytest.mark.skip()
@pytest.mark.parametrize("user_data", invalid_signup_data.values(), ids=invalid_signup_data.keys())
def test_incorrect_signup(make_user, auth_client, user_data):
    user = make_user(username=user_data["username"], password=user_data["password"], autogen=False)
    response = auth_client.register_user_request(user=user)
    assert response.status_code == HTTPStatus.BAD_REQUEST, f"Response schema validation failed: {''.join(response.text)}"


def test_signup_already_registered_user(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    response = auth_client.register_user_request(username=user.username, password=user.password)

    assert response.status_code == HTTPStatus.CONFLICT, f"Expected 409 Conflict, got {response.status_code}"
    assert "Username already exists" in response.json()[
        'message'], "Expected 'Username already exists' message in response"
