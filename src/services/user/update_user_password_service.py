from sqlalchemy.orm import Session
from db_crud.users.update_user_password_crud import update_password_crud
from src.helpers.str_helpers import validate_password


def update_password_service(
    db: Session,
    user_id: int,
    old_password: str,
    new_password: str
):
    """
    Service function to update a user's password.
    Performs input validation and error normalization.
    """

    # Validate user_id
    if not isinstance(user_id, int) or user_id <= 0:
        raise ValueError("User ID must be a positive integer")

    # Validate passwords
    if not old_password or not isinstance(old_password, str):
        raise ValueError("Old password is required")

    # New password must satisfy security rules
    validated_new_password = validate_password(new_password)

    try:
        update_password_crud(
            db=db,
            user_id=user_id,
            old_password=old_password,
            new_password=validated_new_password,
        )

    except ValueError as e:
        # catch: "User not found" or "Incorrect old password"
        raise ValueError(e)
    
    except Exception as e:
        # Unexpected DB failure
        raise RuntimeError(f"Failed to update password: {e}")
