"""
mlte/user/model_logic.py

User model conversions and comparisons.
"""


from mlte.user import passwords
from mlte.user.model import BasicUser, User, UserCreate


def convert_user_create_to_user(user_create: UserCreate) -> User:
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
