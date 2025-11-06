from sqlalchemy.orm import Session
from src.models.factory_model import Factory
from sqlalchemy.exc import IntegrityError


def create_factory_crud(
    db: Session,
    name: str,
    location: str,
    description: str,
    owner_id: int,
) -> Factory:
    
    factory = Factory(
        name=name,
        location=location,
        description=description,
        owner_id=owner_id
    )

    try:
        db.add(factory)
        db.commit()
        db.refresh(factory)
        return factory
    
    except IntegrityError as e:
        db.rollback()
        raise ValueError("Failed to create factory") from e