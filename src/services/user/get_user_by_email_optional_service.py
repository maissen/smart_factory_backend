from sqlalchemy.orm import Session
from src.exceptions.user_exceptions import UserFetchError
from src.db_crud.users.get_user_crud import get_user_by_email_crud
from src.helpers.str_helpers import validate_email

def get_user_by_email_optional_service(db: Session, email: str):
    """
    Returns user if found, otherwise None.
    Does NOT raise EmailDoesNotExistError.
    """

    email = validate_email(email)

    try:
        return get_user_by_email_crud(db, email)
    
    except Exception as e:
        raise UserFetchError()
