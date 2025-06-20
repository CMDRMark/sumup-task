import random
import string


def get_random_username(length: int = 5) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))


def get_random_password(length: int = 5) -> str:
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))
