import pytest

from api_clients_and_models.models.bank_account_model import BankAccountCreationInfoModel
from utils.logger import logger
from api_clients_and_models.models.user_model import User


@pytest.fixture(scope="function")
def set_bank_account_creation_info_to_user():
    """
    A pytest fixture that sets bank account creation information for a user.

    Returns:
        function: A function that accepts a User object and optional bank account details
                  (first_name, last_name, initial_deposit, date_of_birth) and updates the
                  user's bank account creation information.
    """
    def _set_info(user: User, first_name=None, last_name=None, initial_deposit=None, date_of_birth=None):
        """
        Sets the bank account creation information for a user.

        Args:
            user (User): The user object to update.
            first_name (str, optional): The first name of the account holder. Defaults to None.
            last_name (str, optional): The last name of the account holder. Defaults to None.
            initial_deposit (int, optional): The initial deposit amount. Defaults to None.
            date_of_birth (str, optional): The date of birth of the account holder. Defaults to None.

        Returns:
            User: The updated user object with bank account creation information set.
        """
        info = BankAccountCreationInfoModel(first_name=first_name, last_name=last_name, initial_deposit=initial_deposit, date_of_birth=date_of_birth)
        user.bank_account_creation_info = info
        logger.info(f"Set bank account creation info for user: {user.username}, info: {info.to_dict()}")
        return user
    return _set_info


@pytest.fixture(scope="function")
def get_registered_and_logged_in_user(auth_client, get_random_existing_registered_user):
    """
    A pytest fixture that retrieves a registered and logged-in user.

    Args:
        auth_client: The authentication client used to set the user's authentication token.
        get_random_existing_registered_user: A fixture that provides a random registered user.

    Returns:
        User: A registered user object with an authentication token set.
    """
    user = get_random_existing_registered_user
    auth_client.set_auth_token_to_user(user=user)
    return user


@pytest.fixture(scope="function")
def get_registered_and_logged_in_user_with_bank_account(auth_client, get_registered_user_with_bank_account):
    """
    A pytest fixture that retrieves a registered and logged-in user with at least one bank account.

    Args:
        auth_client: The authentication client used to set the user's authentication token.
        get_registered_user_with_bank_account: A fixture that provides a registered user with a bank account.

    Returns:
        User: A registered user object with an authentication token and bank account information set.
    """
    user = get_registered_user_with_bank_account
    auth_client.set_auth_token_to_user(user=user)

    return user