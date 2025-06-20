import pytest
from http import HTTPStatus

from api_client.models.bank_account_model import BankAccountInfoResponseModel
from utils.custom_asserts import assert_response_schema


def test_create_bank_account_for_new_user(bank_account_client, get_new_registered_and_logged_in_user,
                                          set_bank_account_creation_info_to_user, save_registered_user):
    user = get_new_registered_and_logged_in_user
    set_bank_account_creation_info_to_user(user=user, first_name="John", last_name="Doe", initial_deposit=1000,
                                           date_of_birth="1990-01-01")

    response = bank_account_client.create_bank_account(user=user)

    assert_response_schema(model=BankAccountInfoResponseModel, response=response, expected_status=HTTPStatus.OK)
    bank_account_info = BankAccountInfoResponseModel.model_validate(response.json()).to_bank_account()

    user.bank_accounts[bank_account_info.id] = bank_account_info
    save_registered_user(user=user)


def test_create_bank_account_for_existing_user(bank_account_client, get_registered_and_logged_in_user,
                                               set_bank_account_creation_info_to_user,
                                               save_registered_user):
    user = get_registered_and_logged_in_user
    if user.bank_account_creation_info_is_empty():
        set_bank_account_creation_info_to_user(user=user, first_name="John", last_name="Doe", initial_deposit=1000,
                                               date_of_birth="1990-01-01")

    response = bank_account_client.create_bank_account(user=user)

    assert_response_schema(model=BankAccountInfoResponseModel, response=response, expected_status=HTTPStatus.OK)
    bank_account_info = BankAccountInfoResponseModel.model_validate(response.json()).to_bank_account()

    user.bank_accounts[bank_account_info.id] = bank_account_info
    save_registered_user(user=user)


def test_create_bank_account_with_invalid_data(bank_account_client, get_registered_and_logged_in_user, set_bank_account_creation_info_to_user):
    user = get_registered_and_logged_in_user
    # Set invalid bank account creation info
    set_bank_account_creation_info_to_user(user=user, first_name="John Martin   ", last_name="Doe", initial_deposit=1000,
                                           date_of_birth="1990-01-01")

    response = bank_account_client.create_bank_account(user=user)
