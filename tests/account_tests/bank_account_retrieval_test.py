from http import HTTPStatus

from api_client.models.bank_account_model import BankAccountInfoResponseModel
from utils.custom_asserts import assert_response_schema


def test_retrieve_bank_account_info(bank_account_client, get_registered_and_logged_in_user_with_bank_account):
    user = get_registered_and_logged_in_user_with_bank_account
    bank_account_info = user.get_random_bank_account_info()
    response = bank_account_client.get_bank_account_id(user=user, bank_account_id=str(bank_account_info.id))

    assert_response_schema(model=BankAccountInfoResponseModel, response=response, expected_status=HTTPStatus.OK)
    server_info = BankAccountInfoResponseModel.model_validate(response.json()).to_bank_account()
    assert server_info == bank_account_info, f"Difference: {server_info - bank_account_info}"
