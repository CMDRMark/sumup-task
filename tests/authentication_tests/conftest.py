import pytest
import random

from api_client.auth_api_client import AuthAPIClient
from user_resources.user_model import User
from utils.logger import logger
from utils.signup_utils import get_random_username, get_random_password
from utils.user_data_manager import load_users, save_new_user


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
            logger.info(f"Created new user. 'username: {user.username}, password: {user.password}'")
        return user
    return _make_user


@pytest.fixture(scope="session")
def auth_client(get_base_url):
    return AuthAPIClient(base_url=get_base_url)


@pytest.fixture(scope="function")
def get_random_existing_registered_user(get_env) -> User:
    user = random.choice(load_users(env=get_env))
    logger.info(f"Using existing registered user. username: {user.username}, password: {user.password}")
    return user


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
def save_registered_user(request, get_env, save_registered_users_flag):
    """
    A helper fixture to save a user automatically at teardown,
    IF --save-registered-user is passed.
    """

    container = {"user": None}

    def _set_user(user: User):
        container["user"] = user

    def fin():
        if save_registered_users_flag and container["user"]:
            save_new_user(container["user"], get_env)

    request.addfinalizer(fin)
    return _set_user