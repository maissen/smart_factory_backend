from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.factory_model import Factory


def update_factory_crud(
    db: Session,
    factory_id: int,
    name: str,
    location: str,
    description: str,
) -> Factory:
    
    factory = db.query(Factory).filter(Factory.id == factory_id).first()
    if not factory:
        raise ValueError("Factory not found")

    factory.name = name
    factory.location = location
    factory.description = description

    try:
        db.commit()
        db.refresh(factory)
        return factory
    
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to update factory (possibly owner deleted)") from e
