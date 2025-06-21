import pytest
from http import HTTPStatus

from api_clients_and_models.models.bank_account_model import BankAccountInfoResponseModel
from api_clients_and_models.models.unauthorized_response_model import UnauthorizedResponseModel
from tests.account_tests.conftest import get_registered_and_logged_in_user_with_bank_account
from user_accounts_resources.invalid_data.invalid_bank_account_creation_info import invalid_bank_account_creation_info
from utils.custom_asserts import validate_response_schema, assert_sent_information_equals_to_received_information, \
    validate_incorrect_response


def test_create_bank_account_for_new_user(bank_account_api_client, get_new_registered_and_logged_in_user,
                                          set_bank_account_creation_info_to_user, save_registered_user):
    user = get_new_registered_and_logged_in_user
    set_bank_account_creation_info_to_user(user=user, first_name="John", last_name="Doe", initial_deposit=1000,
                                           date_of_birth="1990-01-01")

    response = bank_account_api_client.create_bank_account(user=user)

    validate_response_schema(model=BankAccountInfoResponseModel, response=response, expected_status=HTTPStatus.OK)

    bank_account_info = BankAccountInfoResponseModel.model_validate(response.json()).to_bank_account()

    assert_sent_information_equals_to_received_information(user.bank_account_creation_info.to_dict(),
                                                           bank_account_info.to_dict(),
                                                           exclude_fields="initial_deposit")

    # TODO: Add initial deposit calculation logic to verify separately

    user.bank_accounts[bank_account_info.id] = bank_account_info
    save_registered_user(user=user)


def test_create_bank_account_for_existing_user(bank_account_api_client, get_registered_and_logged_in_user,
                                               set_bank_account_creation_info_to_user,
                                               save_registered_user):
    user = get_registered_and_logged_in_user
    if user.bank_account_creation_info_is_empty():
        set_bank_account_creation_info_to_user(user=user, first_name="John", last_name="Doe", initial_deposit=1000,
                                               date_of_birth="1990-01-01")

    response = bank_account_api_client.create_bank_account(user=user)

    validate_response_schema(model=BankAccountInfoResponseModel, response=response, expected_status=HTTPStatus.OK)

    bank_account_info = BankAccountInfoResponseModel.model_validate(response.json()).to_bank_account()

    assert_sent_information_equals_to_received_information(user.bank_account_creation_info.to_dict(),
                                                           bank_account_info.to_dict(),
                                                           exclude_fields="initial_deposit")

    # TODO: Add initial deposit calculation logic to verify separately

    user.bank_accounts[bank_account_info.id] = bank_account_info
    save_registered_user(user=user)


@pytest.mark.parametrize("test_params", invalid_bank_account_creation_info.values(),
                         ids=invalid_bank_account_creation_info.keys())
def test_create_bank_account_for_registered_user_with_invalid_data(test_params, bank_account_api_client,
                                                                   get_registered_and_logged_in_user,
                                                                   set_bank_account_creation_info_to_user):
    user = get_registered_and_logged_in_user
    set_bank_account_creation_info_to_user(user=user, first_name=test_params.first_name,
                                           last_name=test_params.last_name,
                                           initial_deposit=test_params.initial_deposit,
                                           date_of_birth=test_params.date_of_birth)

    response = bank_account_api_client.create_bank_account(user=user)

    validate_incorrect_response(response,
                                status=test_params.expected_status_code,
                                message=test_params.expected_error_message)

    # Generic test for incorrect bank account creation data, does not validate response schemas.
    # Some specific errors available in API docs are included in the test data, the rest are generic assumptions.

    # TODO: Incorrect status code returned 411 instead of 400 Bad Request


def test_create_bank_account_without_auth_token(bank_account_api_client,
                                                get_registered_user_with_bank_account):
    user = get_registered_user_with_bank_account
    response = bank_account_api_client.create_bank_account(user=user)

    validate_response_schema(model=UnauthorizedResponseModel, response=response,
                             expected_status=HTTPStatus.FORBIDDEN)


def test_create_bank_account_with_incorrect_auth_token(bank_account_api_client,
                                                       get_registered_and_logged_in_user_with_bank_account):
    user = get_registered_and_logged_in_user_with_bank_account
    user.token += "_"

    response = bank_account_api_client.create_bank_account(user=user)

    validate_response_schema(model=UnauthorizedResponseModel, response=response,
                             expected_status=HTTPStatus.UNAUTHORIZED)
