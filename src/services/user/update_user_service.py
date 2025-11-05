from sqlalchemy.orm import Session

from src.db_crud.users.update_user_crud import update_user_crud
from src.helpers.str_helpers import validate_email, validate_phone_number, normalize_str, is_valid_str

from src.services.user.get_user_by_email_service import get_user_by_email_service
from src.services.user.get_user_by_id_service import get_user_by_id_service
from src.services.user.get_user_by_phone_number_service import get_user_by_phone_number_service

from src.exceptions.user_exceptions import (
    InvalidUserIdError,
    InvalidFullNameError,
    InvalidRoleError,
    EmailAlreadyExistsError,
    PhoneNumberAlreadyExistsError,
    UserUpdateError,
)


def update_user_service(
    db: Session,
    user_id: int,
    full_name: str,
    email: str,
    phone_number: str,
    role: str
):
    # Validate user_id
    if not isinstance(user_id, int) or user_id <= 0:
        raise InvalidUserIdError("User ID must be a valid integer.")

    # Validate full_name
    if not is_valid_str(full_name):
        raise InvalidFullNameError("Full name is invalid.")
    full_name = normalize_str(full_name)

    # Validate email & phone
    validated_email = validate_email(email)
    validated_phone = validate_phone_number(phone_number)

    # Ensure user exists
    user = get_user_by_id_service(db=db, user_id=user_id)

    # Check email conflict
    existing_email_user = get_user_by_email_service(db=db, email=validated_email)
    if existing_email_user and existing_email_user.id != user_id:
        raise EmailAlreadyExistsError(f"Email is already in use by another user.")

    # Check phone conflict (409)
    existing_phone_user = get_user_by_phone_number_service(db=db, phone_number=validated_phone)
    if existing_phone_user and existing_phone_user.id != user_id:
        raise PhoneNumberAlreadyExistsError(f"Phone number is already in use by another user.")

    # Validate role if needed
    if not is_valid_str(role):
        raise InvalidRoleError("User role must be a non-empty string.")

    # Perform update
    try:
        updated_user = update_user_crud(
            db=db,
            user_id=user_id,
            full_name=full_name,
            email=validated_email,
            phone_number=validated_phone,
            role=role,
        )

    except Exception as e:
        raise UserUpdateError(f"Failed to update user.")

    return updated_user
