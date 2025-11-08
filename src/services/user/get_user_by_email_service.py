from sqlalchemy.orm import Session

from src.db_crud.users.get_user_crud import get_user_by_email_crud

from src.helpers.str_helpers import validate_email
from src.exceptions.user_exceptions import (
    EmailDoesNotExistError,
    UserFetchError
)


def get_user_by_email_service(db: Session, email: str):
    """
    Service function to retrieve a user by email with domain-correct exceptions.
    
    Steps:
    1. Validate email input using validate_email() 
       - Raises InvalidEmailError if email is missing or invalid.
    2. Fetch user through the CRUD function
       - Wrap unexpected DB/system issues as UserFetchError (500).
    3. If no user is found, raise EmailDoesNotExistError (404).
    """

    # Validate email
    email = validate_email(email)

    # Attempt DB fetch
    try:
        user = get_user_by_email_crud(db, email)

    except Exception as e:
        # Convert unexpected DB errors to a domain-specific operational error
        raise UserFetchError()

    # Not found → email does not exist (404)
    if user is None:
        raise EmailDoesNotExistError()

    return user
