from http import HTTPStatus

from api_clients_and_models.models.bank_account_model import BankAccountInfoResponseModel
from api_clients_and_models.models.unauthorized_response_model import UnauthorizedResponseModel
from utils.custom_asserts import validate_response_schema


def test_get_bank_account_info(bank_account_api_client, get_registered_and_logged_in_user_with_bank_account):
    user = get_registered_and_logged_in_user_with_bank_account
    bank_account_info = user.get_random_bank_account_info()
    response = bank_account_api_client.get_bank_account_id(user=user, bank_account_id=str(bank_account_info.id))

    validate_response_schema(model=BankAccountInfoResponseModel, response=response, expected_status=HTTPStatus.OK)

    server_info = BankAccountInfoResponseModel.model_validate(response.json()).to_bank_account()
    assert server_info == bank_account_info, f"Difference: {server_info - bank_account_info}"

    # Test fails because created_at received during account creation is different from the one received during account info retrieval
    # Need to get more information about the server's behavior regarding created_at field
    # IBAN numbers are compared only if local and server bank account info have them
    # IBAN status is not compared, since it can change asynchronously on server side


def test_get_bank_account_info_without_auth_token(bank_account_api_client, get_registered_user_with_bank_account):
    # Test fails because this endpoint is not secured as it should, based on the current API design
    user = get_registered_user_with_bank_account
    bank_account_info = user.get_random_bank_account_info()

    response = bank_account_api_client.get_bank_account_id(user=user, bank_account_id=str(bank_account_info.id))
    validate_response_schema(model=UnauthorizedResponseModel, response=response, expected_status=HTTPStatus.UNAUTHORIZED)


def test_get_bank_account_info_with_incorrect_auth_token(bank_account_api_client, get_registered_and_logged_in_user_with_bank_account):
    # Test fails because this endpoint is not secured as it should, based on the current API design

    user = get_registered_and_logged_in_user_with_bank_account
    bank_account_id = user.get_random_bank_account_id()

    user.token += "_"

    response = bank_account_api_client.get_bank_account_id(user=user, bank_account_id=str(bank_account_id))
    validate_response_schema(model=UnauthorizedResponseModel, response=response, expected_status=HTTPStatus.UNAUTHORIZED)
