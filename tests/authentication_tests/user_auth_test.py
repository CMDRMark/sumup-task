import pytest
from http import HTTPStatus
from api_clients_and_models.models.login_models import LoginResponseModel
from api_clients_and_models.models.unauthorized_response_model import UnauthorizedResponseModel
from test_data.invalid_data.invalid_user_auth_data import invalid_login_data
from utils.custom_asserts import validate_response_schema, validate_incorrect_response


@pytest.mark.prod_safe
def test_correct_login(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    response = auth_client.login_user_request(username=user.username, password=user.password)

    validate_response_schema(model=LoginResponseModel, response=response, expected_status=HTTPStatus.OK)


def test_login_with_newly_created_user(auth_client, register_new_user, save_registered_user):
    user = register_new_user
    response = auth_client.login_user_request(username=user.username, password=user.password)

    validate_response_schema(model=LoginResponseModel, response=response, expected_status=HTTPStatus.OK)
    save_registered_user(user)


@pytest.mark.parametrize("test_params", invalid_login_data.values(), ids=invalid_login_data.keys())
def test_incorrect_login(make_user, auth_client, test_params):
    # Generic test for incorrect login data, does not validate response schemas,
    # since this endpoint is out of test task scope

    response = auth_client.login_user_request(username=test_params.username, password=test_params.password)

    validate_incorrect_response(response=response, status=test_params.status_code,
                                message=test_params.expected_message)


def test_login_with_incorrect_password(auth_client, get_random_existing_registered_user):
    # Test fails since no response body is returned for this specific case.

    user = get_random_existing_registered_user
    response = auth_client.login_user_request(username=user.username, password=f"{user.password}123")

    validate_response_schema(UnauthorizedResponseModel, response, expected_status=HTTPStatus.UNAUTHORIZED)
