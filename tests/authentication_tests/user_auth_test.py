import pytest
from http import HTTPStatus
from api_clients_and_models.models.login_models import LoginResponseModel
from api_clients_and_models.models.unauthorized_response_model import UnauthorizedResponseModel
from user_accounts_resources.invalid_data.invalid_user_auth_data import invalid_login_data
from utils.custom_asserts import validate_response_schema, validate_incorrect_response


@pytest.mark.prod_safe
def test_correct_login(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    response = auth_client.login_user_request(user=user)

    validate_response_schema(LoginResponseModel, response, expected_status=HTTPStatus.OK)


def test_login_with_newly_created_user(auth_client, register_new_user):
    user = register_new_user
    response = auth_client.login_user_request(user=user)

    validate_response_schema(LoginResponseModel, response, expected_status=HTTPStatus.OK)


@pytest.mark.parametrize("scenario_params", invalid_login_data.values(), ids=invalid_login_data.keys())
def test_incorrect_login(make_user, auth_client, scenario_params):
    response = auth_client.login_user_request(username=scenario_params.username, password=scenario_params.password)

    validate_incorrect_response(response, status=scenario_params.status_code, message=scenario_params.expected_message)
    # Generic test for incorrect login data, does not validate response schema, since this endpoint is out of test task scope


def test_login_with_incorrect_password(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    response = auth_client.login_user_request(username=user.username, password=f"{user.password}123")

    validate_response_schema(UnauthorizedResponseModel, response, expected_status=HTTPStatus.UNAUTHORIZED)
