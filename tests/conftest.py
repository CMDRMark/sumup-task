import pytest
import os

from api_clients_and_models.models.bank_account_model import BankAccountCreationInfoModel
from api_clients_and_models.models.user_model import User
from utils.signup_utils import get_random_username, get_random_password
from utils.user_data_manager import load_users, save_new_user, select_random_user
from utils.logger import logger
from api_clients_and_models.auth_api_client import AuthAPIClient
from api_clients_and_models.bank_account_manager_api_client import BAMAPIClient


@pytest.fixture(scope="function")
def get_random_existing_registered_user(get_env) -> User:
    users = load_users(env=get_env)
    user = select_random_user(users, must_have_bank_account=False)

    logger.info(
        f"Using existing registered user. "
        f"username: {user.username}, "
        f"password: {'***' if os.getenv('HIDE_SECRETS') else user.password}"
    )
    return user


@pytest.fixture(scope="function")
def get_registered_user_with_bank_account(get_env) -> User:
    users = load_users(env=get_env)
    return select_random_user(users, must_have_bank_account=True)


@pytest.fixture(scope="session")
def auth_client(get_base_url):
    return AuthAPIClient(base_url=get_base_url)


@pytest.fixture(scope="session")
def bank_account_api_client(get_base_url):
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
