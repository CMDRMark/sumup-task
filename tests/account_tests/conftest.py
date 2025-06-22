import pytest

from api_clients_and_models.models.bank_account_model import BankAccountCreationInfoModel
from utils.logger import logger
from api_clients_and_models.models.user_model import User


@pytest.fixture(scope="function")
def set_bank_account_creation_info_to_user():
    def _set_info(user: User, first_name=None, last_name=None, initial_deposit=None, date_of_birth=None):
        info = BankAccountCreationInfoModel(first_name=first_name, last_name=last_name, initial_deposit=initial_deposit, date_of_birth=date_of_birth)
        user.bank_account_creation_info = info
        logger.info(f"Set bank account creation info for user: {user.username}, info: {info.to_dict()}")
        return user
    return _set_info


@pytest.fixture(scope="function")
def get_registered_and_logged_in_user(auth_client, get_random_existing_registered_user):
    user = get_random_existing_registered_user
    auth_client.set_auth_token_to_user(user=user)
    return user


@pytest.fixture(scope="function")
def get_registered_and_logged_in_user_with_bank_account(auth_client, get_registered_user_with_bank_account):
    user = get_registered_user_with_bank_account
    auth_client.set_auth_token_to_user(user=user)

    return user
