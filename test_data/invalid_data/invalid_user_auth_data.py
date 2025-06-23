from http import HTTPStatus
from typing import Any
from dataclasses import dataclass


@dataclass
class InvalidLoginData:
    """Represents set of data for invalid login test scenarios."""
    username: Any
    password: Any
    expected_status: HTTPStatus = HTTPStatus.UNAUTHORIZED
    expected_message: str = "Invalid credentials"


invalid_login_data = {
    "NO Password": InvalidLoginData(username="arman_not_registered_0006996", password=""),
    "NO Username": InvalidLoginData(username="", password="arman_not_registered_5767567"),
    "Empty Password": InvalidLoginData(username="arman_not_registered097605", password=" "),
    "Empty Username": InvalidLoginData(username=" ", password="arman_not_registered_75675"),
    "Space in Username": InvalidLoginData(username="test arman_not_registered_76576", password="testpassword"),
    "Space in Password": InvalidLoginData(username="arman_not_registered_345345", password="test password"),
    "Integer username": InvalidLoginData(username=123456789, password="testpassword"),
    "Integer password": InvalidLoginData(username="arman_not_registered_3453445", password=123456789),
    "Special characters in username": InvalidLoginData(username="arman_not_registered_0!@#", password="testpassword"),
    "Special characters in password": InvalidLoginData(username="arman_not_registered_908964", password="testpassword!@#"),
    "Long username": InvalidLoginData(username="a" * 256, password="testpassword"),
    "Long password": InvalidLoginData(username="arman_not_registered_5434543", password="a" * 256),
    "Dictionary username": InvalidLoginData(username={"key": "value"}, password="testpassword"),
    "Dictionary password": InvalidLoginData(username="arman_not_registered_5324", password={"key": "value"}),
    "List username": InvalidLoginData(username=["test", "arman_not_registered_41223"], password="testpassword"),
    "List password": InvalidLoginData(username="arman_not_registered_01233", password=["test", "password"]),
    "None username": InvalidLoginData(username=None, password="testpassword"),
    "None password": InvalidLoginData(username="arman_not_registered_1230", password=None),
    "Boolean username": InvalidLoginData(username=True, password="testpassword"),
    "Boolean password": InvalidLoginData(username="arman_not_registered_0", password=False),
}


@dataclass
class InvalidSignupData:
    """Represents set of data for invalid signup test scenarios."""
    username: Any
    password: Any
    expected_status: HTTPStatus = HTTPStatus.BAD_REQUEST
    expected_message: str = "Invalid input data"


invalid_signup_data = {
    "NO Password": InvalidSignupData(username="arman_not_registered__0", password=""),
    "NO Username": InvalidSignupData(username="", password="arman_not_registered_0"),
    "Empty Password": InvalidSignupData(username="arman_not_registered___0", password=" "),
    "Empty Username": InvalidSignupData(username=" ", password="arman_not_registered_____0"),
    "Space in Username": InvalidSignupData(username="test arman_not_registered_04", password="testpassword"),
    "Space in Password": InvalidSignupData(username="arman_not_registered_05", password="test password"),
    "Integer username": InvalidSignupData(username=123456789, password="testpassword"),
    "Integer password": InvalidSignupData(username="arman_not_registered_6", password=123456789),
    "Special characters in username": InvalidSignupData(username="arman_not_registered_0!@#", password="testpassword"),
    "Special characters in password": InvalidSignupData(username="arman_not_registered_7", password="testpassword!@#"),
    "Long username": InvalidSignupData(username="a" * 256, password="testpassword"),
    "Long password": InvalidSignupData(username="arman_not_registered_9", password="a" * 256),
    "Dictionary username": InvalidSignupData(username={"key": "value"}, password="testpassword"),
    "Dictionary password": InvalidSignupData(username="arman_not_registered_11", password={"key": "value"}),
    "List username": InvalidSignupData(username=["test", "arman_not_registered12"], password="testpassword"),
    "List password": InvalidSignupData(username="arman_not_registered_13", password=["test", "password"]),
    "None username": InvalidSignupData(username=None, password="testpassword"),
    "None password": InvalidSignupData(username="arman_not_registered_14", password=None),
    "Boolean username": InvalidSignupData(username=True, password="testpassword"),
    "Boolean password": InvalidSignupData(username="arman_not_registered_61", password=False),
}
