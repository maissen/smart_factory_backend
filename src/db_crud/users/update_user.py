from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.models.user_model import User
from src.core.settings import settings

def update_user(db: Session, user_id: int, **kwargs) -> User:
    """
    kwargs can include: Full_name, email, phone_number, role
    """
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    if 'role' in kwargs and kwargs['role'] not in settings.USER_ALLOWED_ROLES:
        raise ValueError(f"Role must be one of {settings.USER_ALLOWED_ROLES}")

    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Email or phone number already exists") from e
