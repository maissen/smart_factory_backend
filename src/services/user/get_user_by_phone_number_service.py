from sqlalchemy.orm import Session
from src.db_crud.users.get_user_crud import get_user_by_phone_number_crud


def get_user_by_phone_number_service(db: Session, phone_number: str):
    """
    Service function to retrieve a user by phone number.
    """

    if not isinstance(phone_number, str) or not phone_number.strip() or phone_number == "":
        raise ValueError("Phone number must be a non-empty string")

    try:
        user = get_user_by_phone_number_crud(db, phone_number)

    except Exception as e:
        raise RuntimeError(f"Failed to fetch user by phone number: {e}")

    if user is None:
        raise LookupError("User not found")

    return user
