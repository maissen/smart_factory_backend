from sqlalchemy.orm import Session
from src.models.user_model import User
from src.helpers.auth import get_password_hash

def update_password_crud(db: Session, user_id: int, new_password: str) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    user.password_hash = get_password_hash(plain_password=new_password)
    db.commit()