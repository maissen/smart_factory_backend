from sqlalchemy.orm import Session
from src.db_crud.users.get_user_crud import get_all_users_crud
from src.helpers.str_helpers import is_valid_str

from src.exceptions.user_exceptions import (
    InvalidRoleError,
    UserFetchError
)


def get_all_users_service(db: Session, role: str | None = None):
    """
    Service function to retrieve all users, optionally filtered by role.
    Includes validation and controlled exception behavior.

    Raises:
        InvalidRoleError: If role is not a string.
        EmptyRoleError: If role is an empty or whitespace-only string.
        UserFetchError: If database operation fails.
    """

    # Validate role input
    if not is_valid_str():
        raise InvalidRoleError("Role must be a non-empty string.")

    try:
        users = get_all_users_crud(db, role)
        return users

    except Exception as exc:
        # Bubble the underlying DB issue inside UserFetchError
        raise UserFetchError(f"Failed to fetch users")
