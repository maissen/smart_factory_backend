from sqlalchemy.orm import Session
from src.db_crud.users.get_user_crud import get_user_by_phone_number_crud
from src.helpers.str_helpers import validate_phone_number
from src.exceptions.user_exceptions import (
    PhoneNumberDoesNotExistError,
    UserFetchError
)


def get_user_by_phone_number_service(db: Session, phone_number: str):
    """
    Service function to retrieve a user by phone number.
    """

    # Validate phone number using the helper
    cleaned_phone = validate_phone_number(phone_number)

    # Attempt to fetch user from database
    try:
        user = get_user_by_phone_number_crud(db, cleaned_phone)

    except Exception as e:
        # Wrap any DB/ORM exception in a custom operation error
        raise UserFetchError(f"Failed to fetch user")

    # Check if user exists
    if user is None:
        raise PhoneNumberDoesNotExistError(f"Failed to fetch user")

    return user
