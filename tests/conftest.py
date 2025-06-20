import pytest
import random
import os

from api_client.models.bank_account_model import BankAccount, BankAccountCreationInfoModel
from api_client.models.user_model import User
from utils.signup_utils import get_random_username, get_random_password
from utils.user_data_manager import load_users, save_new_user
from utils.logger import logger
from api_client.auth_api_client import AuthAPIClient
from api_client.bank_account_manager_api_client import BAMAPIClient


def _select_random_user(users: dict, must_have_bank_account: bool = False) -> User:
    """
    Selects a random user from the given users.
    Parses nested objects properly: bank_accounts and bank_account_creation_info.
    Handles missing or empty cases gracefully.
    """
    if must_have_bank_account:
        users = {
            uid: u for uid, u in users.items()
            if u.get("bank_accounts") and len(u["bank_accounts"]) > 0
        }

    if not users:
        raise ValueError(
            "No registered users{} found in the environment data.".format(
                " with bank accounts" if must_have_bank_account else ""
            )
        )

    index = random.choice(list(users.keys()))
    user_data = users[index]

    if user_data.get("bank_accounts"):
        raw_accounts = user_data["bank_accounts"]
        if isinstance(raw_accounts, dict) and raw_accounts:
            user_data["bank_accounts"] = {
                k: BankAccount(**v) for k, v in raw_accounts.items()
            }

    if user_data.get("bank_account_creation_info"):
        raw_info = user_data["bank_account_creation_info"]
        if raw_info is not None:
            user_data["bank_account_creation_info"] = BankAccountCreationInfoModel(**raw_info)

    return User(**user_data)


@pytest.fixture(scope="function")
def get_random_existing_registered_user(get_env) -> User:
    users = load_users(env=get_env)
    user = _select_random_user(users, must_have_bank_account=False)

    logger.info(
        f"Using existing registered user. "
        f"username: {user.username}, "
        f"password: {'***' if os.getenv('HIDE_SECRETS') else user.password}"
    )
    return user


@pytest.fixture(scope="function")
def get_registered_user_with_bank_account(get_env) -> User:
    users = load_users(env=get_env)
    return _select_random_user(users, must_have_bank_account=True)


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
            logger.info(f"Using provided user. 'username: {user.username}, password: {user.password if os.getenv('HIDE_SECRETS') else '***'}")
        else:
            logger.info(f"Generated new user credentials. 'username: {user.username}, password: {user.password if os.getenv('HIDE_SECRETS') else '***'}")
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
