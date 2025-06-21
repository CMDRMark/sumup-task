from http import HTTPStatus
from dataclasses import dataclass

from requests import Response

from api_clients_and_models.models.user_model import User
from utils.custom_requests import post_request


# TODO: no versioning in the api endpoints/headers
# TODO: In the signup endpoint possible issue 2 /api/


@dataclass
class AuthEndpoints:
    base_url: str

    @property
    def login(self) -> str:
        return f"{self.base_url}/api/auth/login"

    @property
    def signup(self) -> str:
        return f"{self.base_url}/api/auth/api/signup"


class AuthAPIClient:
    def __init__(self, base_url: str):
        self.urls = AuthEndpoints(base_url)
        self.headers: dict = {"Content-Type": "application/json"}

    def register_user_request(self, user: User = None, username=None, password=None) -> Response:

        username = username or user.username
        password = password or user.password

        resp = post_request(url=self.urls.signup, json={"username": username, "password": password},
                            headers=self.headers, verify=False)

        if resp.status_code == HTTPStatus.OK:
            user.id = resp.json()["id"]
        return resp

    def login_user_request(self, user: User = None, username=None, password=None) -> Response:

        username = username or user.username
        password = password or user.password

        resp = post_request(url=self.urls.login, headers=self.headers,
                            json={"username": username, "password": password}, verify=False)

        if resp.status_code == HTTPStatus.OK:
            user.token = resp.json()["api_key"]

        return resp
