from sqlalchemy.orm import Session
from src.db_crud.users.delete_user_crud import delete_user_crud
from src.services.user.get_user_by_id_service import get_user_by_id_service

from src.exceptions.user_exceptions import (
    InvalidUserIdError,
    UserNotFoundError,
    UserDeletionError
)


def delete_user_by_id_service(db: Session, user_id: int) -> None:
    """
    Service function responsible for:
    - Validating input
    - Ensuring user exists (delegates to get_user_by_id_service)
    - Delegating deletion to CRUD layer

    Raises:
        InvalidUserIdError
        UserNotFoundError
        UserDeletionError
    """

    # Validate user_id
    if not isinstance(user_id, int) or user_id <= 0:
        raise InvalidUserIdError("User ID must be a positive integer.")

    # Ensure user exists and let the underlying service raise UserNotFoundError if needed
    get_user_by_id_service(db=db, user_id=user_id)

    # Try deleting user
    try:
        delete_user_crud(db, user_id)

    except Exception as e:
        raise UserDeletionError(f"Failed to delete user with ID {user_id}: {e}") from e
