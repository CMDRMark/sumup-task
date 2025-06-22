from http import HTTPStatus

from api_clients_and_models.models.bank_account_model import BankAccountInfoResponseModel
from api_clients_and_models.models.unauthorized_response_model import UnauthorizedResponseModel
from utils.custom_asserts import validate_response_schema


def test_get_bank_account_info(bank_account_api_client, get_registered_and_logged_in_user_with_bank_account):
    user = get_registered_and_logged_in_user_with_bank_account
    bank_account_info = user.get_random_bank_account_info()
    response = bank_account_api_client.get_bank_account_id_request(user=user, bank_account_id=str(bank_account_info.id))

    validate_response_schema(model=BankAccountInfoResponseModel, response=response, expected_status=HTTPStatus.OK)

    server_info = BankAccountInfoResponseModel.model_validate(response.json()).to_bank_account()
    assert server_info == bank_account_info, f"Difference: {server_info - bank_account_info}"


def test_get_bank_account_info_without_auth_token(bank_account_api_client, get_registered_user_with_bank_account):
    user = get_registered_user_with_bank_account
    bank_account_info = user.get_random_bank_account_info()

    response = bank_account_api_client.get_bank_account_id_request(user=user,
                                                                   bank_account_id=str(bank_account_info.id))
    validate_response_schema(model=UnauthorizedResponseModel,
                             response=response,
                             expected_status=HTTPStatus.UNAUTHORIZED)


def test_get_bank_account_info_with_incorrect_auth_token(bank_account_api_client,
                                                         get_registered_and_logged_in_user_with_bank_account):
    user = get_registered_and_logged_in_user_with_bank_account
    bank_account_id = user.get_random_bank_account_id()

    user.token += "_"

    response = bank_account_api_client.get_bank_account_id_request(user=user,
                                                                   bank_account_id=str(bank_account_id))
    validate_response_schema(model=UnauthorizedResponseModel,
                             response=response,
                             expected_status=HTTPStatus.UNAUTHORIZED)
