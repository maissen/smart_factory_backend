from sqlalchemy.orm import Session

from src.models.factory_model import Factory


def delete_factory_crud(db: Session, factory_id: int) -> None:
    factory = db.query(Factory).filter(Factory.id == factory_id).first()
    if not factory:
        raise ValueError("Factory not found")

    db.delete(factory)
    db.commit()
