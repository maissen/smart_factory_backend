from sqlalchemy.orm import Session
from src.models.user_model import User
from src.helpers.auth import verify_password, get_password_hash

def update_password(db: Session, user_id: int, old_password: str, new_password: str) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    if not verify_password(old_password, user.password_hash):
        raise ValueError("Incorrect old password")
    
    user.password_hash = get_password_hash(plain_password=new_password)
    db.commit()