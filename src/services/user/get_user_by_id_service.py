from sqlalchemy.orm import Session
from src.db_crud.users.get_user_crud import get_user_by_id_crud

from src.exceptions.user_exceptions import (
    InvalidUserIdError,
    UserNotFoundError,
    UserFetchError
)


def get_user_by_id_service(db: Session, user_id: int):
    """
    Service function to retrieve a user by ID.
    Performs validation and controlled exception handling.

    Raises:
        InvalidUserIdError: If the provided user_id is not valid.
        UserFetchError: If an unexpected database/system error occurs.
        UserNotFoundError: If no user exists with the given user_id.
    """

    # Input validation
    if not isinstance(user_id, int):
        raise InvalidUserIdError("User ID must be an integer.")

    if user_id <= 0:
        raise InvalidUserIdError("User ID must be a positive integer.")

    # Database call with controlled error handling
    try:
        user = get_user_by_id_crud(db, user_id)

    except Exception as e:
        # Database or internal failure
        raise UserFetchError(f"Failed to fetch user.")

    # Handle missing user
    if user is None:
        raise UserNotFoundError(f"User does not exist.")

    return user
