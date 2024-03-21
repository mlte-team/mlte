###################
# TODO MOVE to STORE
from __future__ import annotations

from typing import Any, Optional

from mlte.user.model import User, StoredUser

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


def get_user(username: Optional[str]) -> Optional[User]:
    if username is not None and username in fake_users_db:
        user_dict: dict[str, Any] = fake_users_db[username]
        return User(**user_dict)
    else:
        return None


def get_user_in_db(username: str) -> Optional[StoredUser]:
    if username in fake_users_db:
        user_dict: dict[str, Any] = fake_users_db[username]
        return StoredUser(**user_dict)
    else:
        return None


###################
