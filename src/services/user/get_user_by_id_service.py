from sqlalchemy.orm import Session
from db_crud.users.get_user_crud import get_user_by_id_crud


def get_user_by_id_service(db: Session, user_id: int):
    """
    Service function to retrieve a user by ID.
    Includes input validation and controlled exception behavior.
    """

    # Validate input
    if not isinstance(user_id, int):
        raise ValueError("User ID must be an integer")

    if user_id <= 0:
        raise ValueError("User ID must be a positive integer")

    try:
        user = get_user_by_id_crud(db, user_id)

    except Exception as e:
        # Database failure or unexpected errors
        raise RuntimeError(f"Failed to fetch user: {e}")

    # User not found case
    if user is None:
        raise LookupError("User not found")

    return user
