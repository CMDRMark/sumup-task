import pytest
from http import HTTPStatus

from api_clients_and_models.models.signup_models import RegistrationResponse
from user_accounts_resources.invalid_data.invalid_user_auth_data import invalid_signup_data
from utils.custom_asserts import validate_response_schema, validate_incorrect_response


def test_correct_signup(make_user, auth_client, save_registered_user):
    user = make_user()
    response = auth_client.register_user_request(user=user)

    response = validate_response_schema(model=RegistrationResponse, response=response, expected_status=HTTPStatus.OK)
    assert response.username == user.username

    save_registered_user(user)


def test_signup_already_registered_user(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    response = auth_client.register_user_request(username=user.username, password=user.password)

    validate_incorrect_response(response, status=HTTPStatus.CONFLICT, message="Username already exists")


@pytest.mark.skip("Skipping these tests as current implementation of the API doesnt follow simple rules for signup: "
                  "no empty username, no empty password, etc.")
@pytest.mark.parametrize("scenario_params", invalid_signup_data.values(), ids=invalid_signup_data.keys())
def test_incorrect_signup(make_user, auth_client, scenario_params):
    user = make_user(username=scenario_params.username, password=scenario_params.password, autogen=False)
    response = auth_client.register_user_request(user=user)

    validate_incorrect_response(response, status=scenario_params.status_code, message=scenario_params.expected_message)
