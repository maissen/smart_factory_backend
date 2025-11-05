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
    role: str
) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    if role not in settings.USER_ALLOWED_ROLES:
        raise ValueError(f"Role must be one of {settings.USER_ALLOWED_ROLES}")

    # Assign blindly
    user.full_name = full_name
    user.email = email
    user.phone_number = phone_number
    user.role = role

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Email or phone number already exists") from e
