import pytest
from pytest_metadata.plugin import metadata_key

from api_clients_and_models.url_mapping import BASE_URLS
from utils.logger import logger
import os

# Set an environment variable to omit URLs in Pydantic error messages
os.environ["PYDANTIC_ERRORS_OMIT_URL"] = "1"


def pytest_addoption(parser):
    """
    Adds custom command-line options to pytest.
    """
    parser.addoption(
        "--env",
        action="store",
        default="TEST",
        choices=["LOCAL", "DEV", "TEST", "STAGING", "PROD"],
        help="""Environment to run tests against (e.g. "LOCAL", "DEV", "TEST", "STAGING", "PROD")"""
    )
    parser.addoption(
        "--save-registered-users",
        action="store_true",
        default=False,
        help="Save registered users to a file for later use"
    )
    parser.addoption(
        "--hide-secrets",
        action="store_true",
        default=False,
        help="Log sensitive information like passwords and tokens as '***' instead of their actual values"
    )


@pytest.fixture(scope='session')
def get_env(request):
    """
    A pytest fixture to retrieve the environment specified via the `--env` CLI option.

    Args:
        request: The pytest request object.

    Returns:
        str: The environment name (e.g., "TEST").
    """
    env = request.config.getoption("--env")
    logger.info(f"Running tests in {env} environment")
    return env


@pytest.fixture(scope='session')
def get_base_url(get_env):
    """
    A pytest fixture to retrieve the base URL for the specified environment.

    Args:
        get_env: A fixture to retrieve the current environment.

    Returns:
        str: The base URL for the environment.
    """
    return BASE_URLS[get_env]


@pytest.fixture(scope='session', autouse=True)
def configure_secrets_logging(request, get_env):
    """
    A pytest fixture to configure logging of sensitive information.

    Args:
        request: The pytest request object.
        get_env: A fixture to retrieve the current environment.
    """
    hide_secrets = request.config.getoption("--hide-secrets")
    if hide_secrets or get_env == "PROD":
        logger.info("Sensitive information will be logged as '***'")
    else:
        logger.info("Sensitive information will be logged in full")
    os.environ["HIDE_SECRETS"] = "1" if hide_secrets else "0"


@pytest.fixture(scope='session')
def save_registered_users_flag(request):
    """
    A pytest fixture to retrieve the `--save-registered-users` flag.

    Args:
        request: The pytest request object.

    Returns:
        bool: True if the flag is set, False otherwise.
    """
    yield request.config.getoption("--save-registered-users")


def pytest_collection_modifyitems(config, items):
    """
    Modifies the test collection based on the environment.

    Args:
        config: The pytest configuration object.
        items: The list of collected test items.
    """
    env = config.getoption("--env")

    if env == "PROD":
        safe_items = []
        skipped_items = []

        for item in items:
            if "prod_safe" in item.keywords:
                safe_items.append(item)
            else:
                skipped_items.append(item)

        if skipped_items:
            for item in skipped_items:
                item.add_marker(pytest.mark.skip(reason="Unsafe for prod"))

        items[:] = safe_items


@pytest.fixture(scope="session", autouse=True)
def push_updated_users_to_vcs():
    """
    A pytest fixture to push updated user data to version control after the test session.
    """
    yield
    logger.info("Pushing updated users to VCS...")


@pytest.hookimpl(tryfirst=True)
def pytest_sessionfinish(session, exitstatus):
    """
    Hook to add custom values to pytest-metadata at the end of the test session.
    """
    config = session.config
    env = config.getoption("--env")
    save_users = config.getoption("--save-registered-users")
    hide_secrets = config.getoption("--hide-secrets", "0")

    if metadata_key in config.stash:
        config.stash[metadata_key]["ENV"] = env
        config.stash[metadata_key]["SAVE REGISTERED USERS"] = save_users
        config.stash[metadata_key]["HIDE SECRETS"] = hide_secrets