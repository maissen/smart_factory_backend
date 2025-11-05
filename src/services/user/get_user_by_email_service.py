from sqlalchemy.orm import Session
from src.db_crud.users.get_user_crud import get_user_by_email_crud


def get_user_by_email(db: Session, email: str):
    """
    Service function to retrieve a user by email.
    Includes basic validation and structured exception behavior.
    """

    # Validate input
    if not isinstance(email, str) or not email.strip() or email == "":
        raise ValueError("Email must be a non-empty string")

    try:
        user = get_user_by_email_crud(db, email)

    except Exception as e:
        raise RuntimeError(f"Failed to fetch user by email: {e}")

    if user is None:
        raise LookupError("User not found")

    return user
