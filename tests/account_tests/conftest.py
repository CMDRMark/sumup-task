import pytest

from api_client.models.bank_account_creation_models import BankAccountCreationInfoModel
from utils.logger import logger
from api_client.models.user_model import User


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
    response = auth_client.login_user_request(user=user)

    if response.status_code == 200:
        logger.info(f"Logged in as existing user: {user.username}")
        return user
    else:
        logger.error(f"Failed to log in as existing user: {user.username}, status code: {response.status_code}")
        return None


@pytest.fixture(scope="function")
def get_registered_and_logged_in_user_with_bank_account(auth_client, get_registered_user_with_bank_account, bank_account_client):
    user = get_registered_user_with_bank_account
    response = auth_client.login_user_request(user=user)
    if response.status_code == 200:
        logger.info(f"Logged in as existing user: {user.username}")
        return user
    else:
        logger.error(f"Failed to log in as existing user: {user.username}, status code: {response.status_code}")
        return None
