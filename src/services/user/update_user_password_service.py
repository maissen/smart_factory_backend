from sqlalchemy.orm import Session
from src.db_crud.users.update_user_password_crud import update_password_crud
from src.helpers.str_helpers import validate_password
from src.services.user.get_user_by_id_service import get_user_by_id_service

from src.helpers.auth import verify_password
from src.exceptions.user_exceptions import (
    InvalidUserIdError,
    MissingPasswordError,
    IncorrectPasswordError,
    PasswordUpdateError
)


def update_password_service(
    db: Session,
    user_id: int,
    old_password: str,
    new_password: str
):
    """
    Service function to update a user's password.
    Performs input validation and error normalization with custom exceptions.
    """

    # Validate user_id
    if not isinstance(user_id, int) or user_id <= 0:
        raise InvalidUserIdError("User ID must be a positive integer.")
    
    validate_password(new_password)
    validate_password(old_password)

    # Validate old_password
    user = get_user_by_id_service(db=db, user_id=user_id)

    if not old_password: # if password is empty
        raise MissingPasswordError("Old password is required.")
    
    if not new_password: # if password is empty
        raise MissingPasswordError("New password is required.")
    
    elif not verify_password(plain_password=old_password, hashed_password=user.password_hash): # compare password hashes
        raise IncorrectPasswordError("Old password is incorrect.")

    # Validate new_password
    validated_new_password = validate_password(new_password)


    # Attempt to update password in DB
    try:
        update_password_crud(
            db=db,
            user_id=user_id,
            new_password=validated_new_password,
        )

    except Exception as e:
        # Catch-all for unexpected DB failures
        raise PasswordUpdateError(f"Failed to update passowrd.")
