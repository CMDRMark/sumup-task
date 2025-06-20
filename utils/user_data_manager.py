import json
from json import JSONDecodeError
from pathlib import Path
from api_client.models.user_model import User
from filelock import FileLock
from utils.logger import logger


def _get_file_path(env: str) -> Path:
    return Path(__file__).parent.parent / "user_accounts_resources" / "registered_users" / f"{env}_ENV_USERS.json"



def load_users(env: str) -> dict:
    file_path = _get_file_path(env)

    if not file_path.exists():
        raise ValueError(f"No user JSON found for env '{env}'")

    lock = FileLock(str(file_path) + ".lock")

    with lock:
        with open(file_path, "r") as f:
            raw_users = json.load(f)

    return raw_users


def save_new_user(user: User, env: str):
    file_path = _get_file_path(env)

    lock = FileLock(str(file_path) + ".lock")

    with lock:
        if not file_path.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)
            with open(file_path, "w") as f:
                json.dump([], f)

        with open(file_path, "r+") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = []
            try:
                users.update(user)
            except TypeError or JSONDecodeError:
                logger.warn(f"Failed to save user '{user}'")
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()


def delete_user(user: User, env: str):
    ...

