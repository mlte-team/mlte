"""
mlte/user/model_logic.py

User model conversions and comparisons.
"""


from typing import Union

from mlte.user import passwords
from mlte.user.model import BasicUser, User, UserCreate


def convert_to_hashed_user(user_create: UserCreate) -> User:
    """Converts a UserCreate model with plain password into a User with a hashed one."""
    # Hash password and create a user with hashed passwords to be stored.
    hashed_password = passwords.hash_password(user_create.password)
    user = User(hashed_password=hashed_password, **user_create.model_dump())
    return user


def are_users_equal(user_create: UserCreate, user: User) -> bool:
    """Compares a UserCreate model with a User, ignoring passwords."""
    return BasicUser(**user_create.model_dump()) == BasicUser(
        **user.model_dump()
    )


def update_user(
    curr_user: User, new_user_data: Union[UserCreate, BasicUser]
) -> User:
    """Returns up updated version of the given user with new data, with or without password, depending on the user type."""
    if type(new_user_data) is UserCreate:
        # In this case, new user fully overwrites existing one.
        updated_user = convert_to_hashed_user(new_user_data)
    elif type(new_user_data) is BasicUser:
        # In this case, all data overwrites the current one, except for the hashed password, which is kept.
        updated_user = User(
            **new_user_data.model_dump(),
            hashed_password=curr_user.hashed_password,
        )
    else:
        raise Exception(
            f"Invalid user type received when updating user type: {type(new_user_data)}"
        )
    return updated_user
