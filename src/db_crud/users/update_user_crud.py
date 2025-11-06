from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.models.user_model import User
from src.core.settings import settings


def update_user_crud(
    db: Session,
    user_id: int,
    full_name: str,
    email: str,
    phone_number: str,
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    # Assign blindly
    user.full_name = full_name
    user.email = email
    user.phone_number = phone_number

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Email or phone number already exists") from e
