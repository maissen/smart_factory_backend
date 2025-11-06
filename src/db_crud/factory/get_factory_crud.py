from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.factory_model import Factory


def get_factory_by_id_crud(db: Session, factory_id: int) -> Factory | None:
    return db.query(Factory).filter(Factory.id == factory_id).first()


def get_factory_of_user_crud(db: Session, user_id: int) -> Factory:
    return db.query(Factory).filter(Factory.owner_id == user_id)


def get_all_factories_crud(db: Session) -> list[Factory]:
    return db.query(Factory).all()