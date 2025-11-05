from sqlalchemy.orm import Session
from src.db_crud.users.get_user_crud import get_user_by_phone_number_crud
from src.helpers.str_helpers import validate_phone_number
from src.exceptions.user_exceptions import UserFetchError


def get_user_by_phone_number_optional_service(db: Session, phone_number: str):
    """
    Service function to retrieve a user by phone number for existence check.
    Returns None if user does not exist. Does NOT raise PhoneNumberDoesNotExistError.
    """

    # Validate phone number
    cleaned_phone = validate_phone_number(phone_number)

    # Attempt to fetch user
    try:
        user = get_user_by_phone_number_crud(db, cleaned_phone)
        return user

    except Exception as e:
        # Wrap unexpected DB errors
        raise UserFetchError(f"Failed to fetch user for phone number existence check: {e}")
