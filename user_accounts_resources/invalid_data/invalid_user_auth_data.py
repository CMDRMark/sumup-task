from http import HTTPStatus
from typing import Any
from dataclasses import dataclass


@dataclass
class InvalidLoginData:
    """Represents a single invalid account creation scenario."""
    username: Any
    password: Any
    expected_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    expected_message: str = "Invalid credentials"


invalid_login_data = {
    "NO Password": InvalidLoginData(username="arman_not_registered", password=""),
    "NO Username": InvalidLoginData(username="", password="arman_not_registered"),
    "Empty Password": InvalidLoginData(username="arman_not_registered", password=" "),
    "Empty Username": InvalidLoginData(username=" ", password="arman_not_registered"),
    "Space in Username": InvalidLoginData(username="test arman_not_registered3", password="testpassword"),
    "Space in Password": InvalidLoginData(username="arman_not_registered3", password="test password"),
    "Integer username": InvalidLoginData(username=123456789, password="testpassword"),
    "Integer password": InvalidLoginData(username="arman_not_registered", password=123456789),
    "Special characters in username": InvalidLoginData(username="arman_not_registered!@#", password="testpassword"),
    "Special characters in password": InvalidLoginData(username="arman_not_registered", password="testpassword!@#"),
    "Long username": InvalidLoginData(username="a" * 256, password="testpassword"),
    "Long password": InvalidLoginData(username="arman_not_registered", password="a" * 256),
    "Dictionary username": InvalidLoginData(username={"key": "value"}, password="testpassword"),
    "Dictionary password": InvalidLoginData(username="arman_not_registered", password={"key": "value"}),
    "List username": InvalidLoginData(username=["test", "arman_not_registered"], password="testpassword"),
    "List password": InvalidLoginData(username="arman_not_registered", password=["test", "password"]),
    "None username": InvalidLoginData(username=None, password="testpassword"),
    "None password": InvalidLoginData(username="arman_not_registered", password=None),
    "Boolean username": InvalidLoginData(username=True, password="testpassword"),
    "Boolean password": InvalidLoginData(username="arman_not_registered", password=False),
}


@dataclass
class InvalidSignupData:
    """Represents a single invalid signup scenario."""
    username: Any
    password: Any
    expected_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    expected_message: str = "Invalid input data"


invalid_signup_data = {
    "NO Password": InvalidSignupData(username="arman_not_registered", password=""),
    "NO Username": InvalidSignupData(username="", password="arman_not_registered"),
    "Empty Password": InvalidSignupData(username="arman_not_registered", password=" "),
    "Empty Username": InvalidSignupData(username=" ", password="arman_not_registered"),
    "Space in Username": InvalidSignupData(username="test arman_not_registered3", password="testpassword"),
    "Space in Password": InvalidSignupData(username="arman_not_registered3", password="test password"),
    "Integer username": InvalidSignupData(username=123456789, password="testpassword"),
    "Integer password": InvalidSignupData(username="arman_not_registered", password=123456789),
    "Special characters in username": InvalidSignupData(username="arman_not_registered!@#", password="testpassword"),
    "Special characters in password": InvalidSignupData(username="arman_not_registered", password="testpassword!@#"),
    "Long username": InvalidSignupData(username="a" * 256, password="testpassword"),
    "Long password": InvalidSignupData(username="arman_not_registered", password="a" * 256),
    "Dictionary username": InvalidSignupData(username={"key": "value"}, password="testpassword"),
    "Dictionary password": InvalidSignupData(username="arman_not_registered", password={"key": "value"}),
    "List username": InvalidSignupData(username=["test", "arman_not_registered"], password="testpassword"),
    "List password": InvalidSignupData(username="arman_not_registered", password=["test", "password"]),
    "None username": InvalidSignupData(username=None, password="testpassword"),
    "None password": InvalidSignupData(username="arman_not_registered", password=None),
    "Boolean username": InvalidSignupData(username=True, password="testpassword"),
    "Boolean password": InvalidSignupData(username="arman_not_registered", password=False),
}
