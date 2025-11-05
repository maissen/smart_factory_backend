from sqlalchemy.orm import Session
from src.models.user_model import User

def delete_user_crud(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    
    db.delete(user)
    db.commit()
