"""
mlte/user/model_logic.py

User model conversions and comparisons.
"""


from mlte.user import passwords
from mlte.user.model import User, UserCreate


def convert_user_create_to_user(user_create: UserCreate) -> User:
    """Converts a UserCreate model with plain password into a User with a hashed one."""
    # Hash password and create a user with hashed passwords to be stored.
    hashed_password = passwords.hash_password(user_create.password)
    user = User(
        username=user_create.username,
        email=user_create.email,
        disabled=user_create.disabled,
        hashed_password=hashed_password,
    )
    return user


def are_users_equal(user_create: UserCreate, user: User) -> bool:
    """Compares a UserCreate model with a User, ignoring passwords."""
    return (
        user.username == user_create.username
        and user.email == user_create.email
        and user.disabled == user_create.disabled
    )
