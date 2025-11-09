from sqlalchemy.orm import Session

from src.db_crud.users.update_user_crud import update_user_crud
from src.helpers.str_helpers import validate_email, validate_phone_number, normalize_str, is_valid_str
from src.helpers.validate_user_id import validate_user_id

from src.services.user.get_user_by_phone_number_optional_service import get_user_by_phone_number_optional_service
from src.services.user.get_user_by_email_optional_service import get_user_by_email_optional_service

from src.services.user.get_user_by_id_service import get_user_by_id_service

from src.exceptions.user_exceptions import (
    InvalidFullNameError,
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
):
    # Validate user_id
    validate_user_id(user_id=user_id)

    # Validate full_name
    if not is_valid_str(full_name):
        raise InvalidFullNameError()
    full_name = normalize_str(full_name)

    # Validate email & phone
    validated_email = validate_email(email)
    validated_phone = validate_phone_number(phone_number)

    # Ensure user exists
    user = get_user_by_id_service(db=db, user_id=user_id)

    # Check email conflict
    existing_email_user = get_user_by_email_optional_service(db=db, email=validated_email)
    if existing_email_user and existing_email_user.id != user_id:
        raise EmailAlreadyExistsError()

    # Check phone conflict (409)
    existing_phone_user = get_user_by_phone_number_optional_service(db=db, phone_number=validated_phone)
    if existing_phone_user and existing_phone_user.id != user_id:
        raise PhoneNumberAlreadyExistsError()

    # Perform update
    try:
        updated_user = update_user_crud(
            db=db,
            user_id=user_id,
            full_name=full_name,
            email=validated_email,
            phone_number=validated_phone,
        )

    except Exception as e:
        raise UserUpdateError()

    return updated_user
