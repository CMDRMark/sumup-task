from http import HTTPStatus
from dataclasses import dataclass

from requests import Response

from api_clients_and_models.models.user_model import User
from utils.custom_requests import post_request


@dataclass
class AuthEndpoints:
    """
    A dataclass to define authentication-related API endpoints.

    Attributes:
        base_url (str): The base URL for the API.
    """
    base_url: str

    @property
    def login(self) -> str:
        """
        Constructs the login endpoint URL.

        Returns:
            str: The login endpoint URL.
        """
        return f"{self.base_url}/api/auth/login"

    @property
    def signup(self) -> str:
        """
        Constructs the signup endpoint URL.

        Returns:
            str: The signup endpoint URL.
        """
        return f"{self.base_url}/api/auth/api/signup"


class AuthAPIClient:
    """
    A client for interacting with authentication-related API endpoints.

    Attributes:
        urls (AuthEndpoints): An instance of AuthEndpoints containing the API URLs.
        headers (dict): Default headers for API requests.
    """

    def __init__(self, base_url: str):
        """
        Initializes the AuthAPIClient with the base URL.

        Args:
            base_url (str): The base URL for the API.
        """
        self.urls = AuthEndpoints(base_url)
        self.headers: dict = {"Content-Type": "application/json"}

    def register_user_request(self, user: User = None, username=None, password=None) -> Response:
        """
        Sends a request to register a new user.

        Args:
            user (User, optional): A User object containing user details. Defaults to None.
            username (str, optional): The username for the new user. Defaults to None.
            password (str, optional): The password for the new user. Defaults to None.

        Returns:
            Response: The HTTP response from the API.

        Raises:
            ValueError: If the response status code is not HTTPStatus.OK.
        """
        username = username or user.username
        password = password or user.password

        resp = post_request(url=self.urls.signup, json={"username": username, "password": password},
                            headers=self.headers, verify=False)

        if resp.status_code == HTTPStatus.OK:
            user.id = resp.json()["id"]
        return resp

    def login_user_request(self, username=None, password=None) -> Response:
        """
        Sends a request to log in a user.

        Args:
            username (str, optional): The username of the user. Defaults to None.
            password (str, optional): The password of the user. Defaults to None.

        Returns:
            Response: The HTTP response from the API.
        """
        resp = post_request(url=self.urls.login, headers=self.headers,
                            json={"username": username, "password": password}, verify=False)

        return resp

    def set_auth_token_to_user(self, user: User) -> None:
        """
        Logs in a user and sets their authentication token.

        Args:
            user (User): The user object to update with the authentication token.

        Raises:
            ValueError: If the login request fails.
        """
        resp = self.login_user_request(username=user.username, password=user.password)

        if resp.status_code == HTTPStatus.OK:
            user.token = resp.json()["api_key"]
        else:
            raise ValueError(f"Failed to log in user {user.username}. Status code: {resp.status_code}, "
                             f"Response: {resp.text}")