import pytest




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