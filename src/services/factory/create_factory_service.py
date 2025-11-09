from sqlalchemy.orm import Session

from src.models.factory_model import Factory
from src.services.user.get_user_by_id_service import get_user_by_id_service
from src.db_crud.factory.create_factory_crud import create_factory_crud
from src.services.factory.get_factory_service import get_factory_of_user_service

from src.exceptions.factory_exceptions import (
    FactoryError,
    FactoryAlreadyExistsError
)


def create_factory_service(
    db: Session,
    name: str,
    location: str,
    description: str,
    owner_id: int,
) -> Factory:
    
    # Validate owner exists
    owner = get_user_by_id_service(db, owner_id)

    # Check if factory already exists for this owner
    existing_factory = get_factory_of_user_service(db=db, user_id=owner_id, raise_error=False)
    if existing_factory:
        raise FactoryAlreadyExistsError()

    # Create factory
    try:
        return create_factory_crud(db, name, location, description, owner_id)
    
    except ValueError:
        raise FactoryError("Failed to create factory.")
