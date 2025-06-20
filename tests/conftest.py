import pytest
import random

from api_client.models.bank_account_creation_models import BankAccountCreationInfoModel
from api_client.models.bank_account_model import BankAccount
from api_client.models.user_model import User
from utils.signup_utils import get_random_username, get_random_password
from utils.user_data_manager import load_users, save_new_user
from utils.logger import logger
from api_client.auth_api_client import AuthAPIClient
from api_client.bank_account_manager_api_client import BAMAPIClient


@pytest.fixture(scope="function")
def get_random_existing_registered_user(get_env) -> User:
    users = load_users(env=get_env)
    index = random.choice(list(users.keys()))
    user = User(**users[index])
    logger.info(f"Using existing registered user. username: {user.username}, password: {user.password}")
    return user


@pytest.fixture(scope="function")
def get_registered_user_with_bank_account(get_env) -> User:
    users = load_users(env=get_env)
    users_with_bank_accounts = {
        user_id: user_data
        for user_id, user_data in users.items()
        if user_data.get("bank_accounts") and len(user_data["bank_accounts"]) > 0
    }

    if not users_with_bank_accounts:
        raise ValueError("No registered users with bank accounts found in the environment data.")

    index = random.choice(list(users_with_bank_accounts.keys()))
    user_data = users_with_bank_accounts[index]

    raw_accounts = user_data["bank_accounts"]
    parsed_accounts = {
        k: BankAccount(**v) for k, v in raw_accounts.items()
    }
    user_data["bank_accounts"] = parsed_accounts
    user = User(**user_data)

    return user


@pytest.fixture(scope="session")
def auth_client(get_base_url):
    return AuthAPIClient(base_url=get_base_url)


@pytest.fixture(scope="session")
def bank_account_client(get_base_url):
    return BAMAPIClient(base_url=get_base_url)


@pytest.fixture
def make_user():
    def _make_user(username=None, password=None, autogen=True):
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
            logger.info(f"Using provided user. 'username: {user.username}, password: {user.password}'")
        else:
            logger.info(f"Generated new user credentials. 'username: {user.username}, password: {user.password}'")
        return user
    return _make_user


@pytest.fixture(scope="function")
def register_new_user(auth_client, make_user, save_registered_user):

    user = make_user()
    response = auth_client.register_user_request(user=user)

    if response.status_code == 200:
        logger.info(f"Registered new user: {user.username}")
        save_registered_user(user)
        return user
    else:
        raise Exception(f"Failed to register user: {response.text}")


@pytest.fixture(scope="function")
def get_new_registered_and_logged_in_user(register_new_user, auth_client, save_registered_user) -> User:
    """
    A fixture to create a new user, register them, and log them in.
    It also saves the user if --save-registered-user is passed.
    """
    user = register_new_user
    auth_client.login_user_request(user=user)
    save_registered_user(user)
    return user



@pytest.fixture(scope="function")
def save_registered_user(request, get_env, save_registered_users_flag):
    """
    A helper fixture to save a user automatically at teardown,
    IF --save-registered-user is passed.
    """

    container = {"user": None}

    def _set_user(user: User):
        if isinstance(user.bank_account_creation_info, BankAccountCreationInfoModel):
            user.bank_account_creation_info = user.bank_account_creation_info.to_dict()
        container["user"] = {str(user.id): user.to_dict()}

    def fin():
        if save_registered_users_flag and container["user"]:
            save_new_user(container["user"], get_env)

    request.addfinalizer(fin)
    return _set_user
