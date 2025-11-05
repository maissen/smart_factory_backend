from sqlalchemy.orm import Session

from db_crud.users.create_user_crud import create_user_crud
from src.helpers.str_helpers import (
    validate_email,
    validate_password,
    validate_phone_number,
    is_valid_str,
    normalize_str
)
from src.services.user import (
    get_user_by_email_service,
    get_user_by_phone_number_service
)

from src.exceptions.user_exceptions import (
    InvalidFullNameError,
    EmailAlreadyExistsError,
    PhoneNumberAlreadyExistsError,
    UserCreationError
)


def create_user_service(
    db: Session,
    full_name: str,
    email: str,
    password: str,
    role: str,
    phone_number: str
):
    """
    Service function that validates inputs, ensures unique user data,
    and calls the CRUD layer to create a new user.
    """

    # Validate full_name
    if not is_valid_str(full_name):
        raise InvalidFullNameError("Full name is required.")

    full_name = normalize_str(full_name)

    # Validate other fields (these functions already raise appropriate exceptions)
    validated_email = validate_email(email)
    validated_password = validate_password(password)
    validated_phone = validate_phone_number(phone_number)

    # Check conflicts (404 getter services likely return None if not found)
    existing_email_user = get_user_by_email_service(db=db, email=validated_email)
    if existing_email_user:
        raise EmailAlreadyExistsError(f"Email is already in use.")

    existing_phone_user = get_user_by_phone_number_service(db=db, phone_number=validated_phone)
    if existing_phone_user:
        raise PhoneNumberAlreadyExistsError(f"Phone number is already in use.")

    # Attempt creation
    try:
        new_user = create_user_crud(
            db=db,
            full_name=full_name,
            email=validated_email,
            password=validated_password,
            role=role,
            phone_number=validated_phone
        )

    except Exception as e:
        # Any unexpected/db-level errors map to HTTP 500
        raise UserCreationError(f"Unexpected error while creating user: {e}")

    return new_user
