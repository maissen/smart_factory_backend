from sqlalchemy.orm import Session

from src.models.factory_model import Factory
from src.services.user.get_user_by_id_service import get_user_by_id_service
from src.db_crud.factory.create_factory_crud import create_factory_crud

from src.exceptions.factory_exceptions import (
    FactoryOwnerNotFoundError,
    FactoryAlreadyExistsError,
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

    if not owner:
        raise FactoryOwnerNotFoundError(owner_id)

    try:
        return create_factory_crud(db, name, location, description, owner_id)
    
    except ValueError:
        raise FactoryAlreadyExistsError("Each user can only has one factory.")