import json
import random
from json import JSONDecodeError
from pathlib import Path

from api_clients_and_models.models.bank_account_model import BankAccount, BankAccountCreationInfoModel
from api_clients_and_models.models.user_model import User
from filelock import FileLock
from utils.logger import logger


def _get_file_path(env: str) -> Path:
    return Path(__file__).parent.parent / "test_data" / "registered_users" / f"{env}_ENV_USERS.json"



def load_users(env: str) -> dict:
    file_path = _get_file_path(env)

    if not file_path.exists():
        logger.info(f"File {file_path} not found. Creating a new one.")
        file_path.parent.mkdir(parents=True, exist_ok=True)

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
                json.dump({}, f)

        with open(file_path, "r+") as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}
            try:
                users.update(user)
            except TypeError or JSONDecodeError:
                logger.warn(f"Failed to save user '{user}'")
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()


def select_random_user(users: dict, must_have_bank_account: bool = False) -> User:
    """
    Selects a random user from the given users.
    Parses nested objects properly: bank_accounts and bank_account_creation_info.
    Handles missing or empty cases gracefully.
    """
    if must_have_bank_account:
        users = {
            uid: u for uid, u in users.items()
            if u.get("bank_accounts") and len(u["bank_accounts"]) > 0
        }

    if not users:
        raise ValueError(
            "No registered users{} found in the environment data.".format(
                " with bank accounts" if must_have_bank_account else ""
            )
        )

    index = random.choice(list(users.keys()))
    user_data = users[index]

    if user_data.get("bank_accounts"):
        raw_accounts = user_data["bank_accounts"]
        if isinstance(raw_accounts, dict) and raw_accounts:
            user_data["bank_accounts"] = {
                k: BankAccount(**v) for k, v in raw_accounts.items()
            }

    if user_data.get("bank_account_creation_info"):
        raw_info = user_data["bank_account_creation_info"]
        if raw_info is not None:
            user_data["bank_account_creation_info"] = BankAccountCreationInfoModel(**raw_info)

    return User(**user_data)


def delete_user(user: User, env: str):
    ...
