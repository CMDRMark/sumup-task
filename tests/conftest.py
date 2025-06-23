from http import HTTPStatus

import pytest
import os

from api_clients_and_models.models.bank_account_model import (
    BankAccountCreationInfoModel,
    BankAccountInfoResponseModel,
)
from api_clients_and_models.models.signup_models import RegistrationResponse
from api_clients_and_models.models.user_model import User
from utils.custom_asserts import (
    validate_response_schema,
    assert_sent_information_equals_to_received_information,
)
from utils.signup_utils import get_random_username, get_random_password
from utils.user_data_manager import load_users, save_new_user, select_random_user
from utils.logger import logger
from api_clients_and_models.auth_api_client import AuthAPIClient
from api_clients_and_models.bank_account_manager_api_client import BAMAPIClient


@pytest.fixture(scope="session")
def auth_client(get_base_url):
    """
    A pytest fixture to create an instance of the AuthAPIClient.

    Args:
        get_base_url: A fixture to retrieve the base URL for the API.

    Returns:
        AuthAPIClient: An instance of the authentication API client.
    """
    return AuthAPIClient(base_url=get_base_url)


@pytest.fixture(scope="session")
def bank_account_api_client(get_base_url):
    """
    A pytest fixture to create an instance of the BAMAPIClient.

    Args:
        get_base_url: A fixture to retrieve the base URL for the API.

    Returns:
        BAMAPIClient: An instance of the bank account manager API client.
    """
    return BAMAPIClient(base_url=get_base_url)


@pytest.fixture(scope="function")
def get_random_existing_registered_user(get_env, register_new_user) -> User:
    """
    A pytest fixture to retrieve a random existing registered user.
    If user file does not exist, it registers a new user, so that tests won't fail.

    Args:
        get_env: A fixture to retrieve the current environment.

    Returns:
        User: A randomly selected registered user object without requiring a bank account.
        :param get_env: fixture to retrieve the current environment.
        :param register_new_user: fixture to register a new user if no users are found.
    """
    users = load_users(env=get_env)

    user = register_new_user if not users else select_random_user(users, must_have_bank_account=False)

    logger.info(
        f"Using existing registered user. "
        f"username: {user.username}, "
        f"password: {'***' if os.getenv('HIDE_SECRETS') else user.password}"
    )
    return user


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
        info = BankAccountCreationInfoModel(first_name=first_name,
                                            last_name=last_name,
                                            initial_deposit=initial_deposit,
                                            date_of_birth=date_of_birth)
        user.bank_account_creation_info = info
        logger.info(f"Set bank account creation info for user: {user.username}, info: {info.to_dict()}")
        return user
    return _set_info


@pytest.fixture(scope="function")
def get_registered_user_with_bank_account(auth_client, bank_account_api_client,
                                          get_env, register_new_user,
                                          set_bank_account_creation_info_to_user, save_registered_user) -> User:
    """
    A pytest fixture to retrieve a random registered user with at least one bank account.

    If no registered users are found, it creates a new user, sets their bank account
    creation information, registers the user, and creates a bank account for them.

    Args:
        auth_client (AuthAPIClient): The authentication client used to authenticate the user.
        bank_account_api_client (BAMAPIClient): The bank account manager API client.
        get_env (str): A fixture to retrieve the current environment.
        register_new_user (User): A fixture to register a new user if no users are found.
        set_bank_account_creation_info_to_user (function): A function to set bank account creation info for a user.
        save_registered_user (function): A function to save the registered user.

    Returns:
        User: A randomly selected registered user object with a bank account.
    """
    users = load_users(env=get_env)
    if not users:
        logger.warning("No registered users found. Registering a new user.")
        # If no users are found, register a new user

        user = register_new_user
        set_bank_account_creation_info_to_user(user,
                                               first_name="John",
                                               last_name="Doe",
                                               initial_deposit=1000,
                                               date_of_birth="1990-01-01")
        auth_client.set_auth_token_to_user(user=user)
        response = bank_account_api_client.create_bank_account_request(user=user)

        bank_account_info = validate_response_schema(
            model=BankAccountInfoResponseModel,
            response=response,
            expected_status=HTTPStatus.OK,
        )

        assert_sent_information_equals_to_received_information(
            user.bank_account_creation_info.to_dict(),
            bank_account_info.to_bank_account().to_dict(),
            exclude_fields="initial_deposit",
        )

        user.bank_accounts[bank_account_info.id] = bank_account_info.to_bank_account()
        save_registered_user(user=user)
        return user

    return select_random_user(users, must_have_bank_account=True)


@pytest.fixture
def make_user():
    """
    A pytest fixture to create a new user object.

    This fixture provides a function to generate a new user with optional
    username and password. If no username or password is provided, random
    values will be generated.

    Returns:
        function: A function that creates a User object with the specified
                  or autogenerated credentials.
    """
    def _make_user(username=None, password=None, autogen=True):
        """
        Creates a User object with the given or autogenerated credentials.

        Args:
            username (str, optional): The username for the user. Defaults to None.
            password (str, optional): The password for the user. Defaults to None.
            autogen (bool, optional): Whether to generate random credentials if
                                      username or password is not provided. Defaults to True.

        Returns:
            User: A User object with the specified or autogenerated credentials.
        """
        if autogen:
            user = User(
                username=username or get_random_username(),
                password=password or get_random_password()
            )
        else:
            user = User(
                username=username,
                password=password
            )
        if password and username:
            logger.info(f"Using provided user. 'username: {user.username}, "
                        f"password: {user.password if os.getenv('HIDE_SECRETS') else '***'}")
        else:
            logger.info(f"Generated new user credentials. 'username: {user.username}, "
                        f"password: {user.password if os.getenv('HIDE_SECRETS') else '***'}")
        return user
    return _make_user


@pytest.fixture(scope="function")
def register_new_user(auth_client, make_user) -> User:
    """
    A pytest fixture to register a new user using the authentication client.

    Args:
        auth_client: The authentication client used to register the user.
        make_user: A fixture to create a new user object.

    Returns:
        User: The newly registered user object.
    """
    user = make_user()
    response = auth_client.register_user_request(user=user)

    signup_response = validate_response_schema(model=RegistrationResponse,
                                               response=response,
                                               expected_status=HTTPStatus.OK)
    assert signup_response.username == user.username

    return user


@pytest.fixture(scope="function")
def get_new_registered_and_logged_in_user(register_new_user, auth_client) -> User:
    """
    A pytest fixture to create a new user, register them, and log them in.

    Args:
        register_new_user: A fixture to register a new user.
        auth_client: The authentication client used to log in the user.

    Returns:
        User: The newly registered and logged-in user object.
    """
    user = register_new_user
    auth_client.set_auth_token_to_user(user=user)

    return user


@pytest.fixture(scope="function")
def save_registered_user(request, get_env, save_registered_users_flag):
    """
    A pytest fixture to save a user automatically during teardown,
    if the `--save-registered-user` flag is passed as a pytest CLI parameter.

    Args:
        request: The pytest request object, used to add a finalizer.
        get_env: A fixture to retrieve the current environment.
        save_registered_users_flag (bool): A flag indicating whether to save registered users.

    Returns:
        function: A function that accepts a User object and prepares it for saving.
    """
    container = {"user": None}

    def _set_user(user: User):
        """
        Prepares a User object for saving by converting its bank account creation info
        to a dictionary if necessary.

        Args:
            user (User): The user object to prepare for saving.
        """
        if isinstance(user.bank_account_creation_info, BankAccountCreationInfoModel):
            user.bank_account_creation_info = user.bank_account_creation_info.to_dict()
        container["user"] = {str(user.id): user.to_dict()}

    def fin():
        """
        Finalizer function to save the user if the `--save-registered-user` flag is set
        and a user has been prepared for saving.
        """
        if save_registered_users_flag and container["user"]:
            save_new_user(container["user"], get_env)

    request.addfinalizer(fin)
    return _set_user