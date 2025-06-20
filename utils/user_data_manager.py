import json
from pathlib import Path
from user_resources.user_model import User
from filelock import FileLock


def load_users(env: str):
    file_path = Path(__file__).parent.parent / "user_resources" / "registered_users" / f"{env}_ENV_USERS.json"

    if not file_path.exists():
        raise ValueError(f"No user JSON found for env '{env}'")

    lock = FileLock(str(file_path) + ".lock")

    with lock:
        with open(file_path, "r") as f:
            raw_users = json.load(f)

    return [User(**user) for user in raw_users]


def save_new_user(user: User, env: str):
    file_path = Path(__file__).parent.parent / "user_resources" / "registered_users" / f"{env}_ENV_USERS.json"

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
            users.append(user.save_to_file())
            f.seek(0)
            json.dump(users, f, indent=4)
            f.truncate()