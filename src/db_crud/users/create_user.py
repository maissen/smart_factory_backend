from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.models.user_model import User
from src.core.settings import settings
from src.helpers.auth import get_password_hash

def create_user(db: Session, full_name: str, email: str, password: str, role: str, phone_number: str) -> User:
    if role not in settings.USER_ALLOWED_ROLES:
        raise ValueError(f"Role must be one of {settings.USER_ALLOWED_ROLES}")

    hashed_password = get_password_hash(password)
    
    new_user = User(
        full_name=full_name,
        email=email,
        password_hash=hashed_password,
        role=role,
        phone_number=phone_number,
    )
    
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError as e:
        db.rollback()
        raise ValueError("User with given email or phone number already exists") from e
