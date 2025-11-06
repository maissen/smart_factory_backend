from sqlalchemy.orm import Session

from src.models.factory_model import Factory
from src.services.user.get_user_by_id_service import get_user_by_id_service
from src.db_crud.factory.get_factory_crud import (
    get_factory_by_id_crud,
)
from src.db_crud.factory.update_factory_crud import update_factory_crud
from src.exceptions.factory_exceptions import (
    FactoryNotFoundError,
    FactoryPermissionError,
    FactoryUpdateError,
)

def update_factory_service(
    db: Session,
    factory_id: int,
    user_id: int,
    name: str,
    location: str,
    description: str,
) -> Factory:
    
    factory = get_factory_by_id_crud(db, factory_id)
    if not factory:
        raise FactoryNotFoundError(factory_id)

    # Permission check
    if factory.owner_id != user_id:
        raise FactoryPermissionError(user_id, factory_id)

    try:
        return update_factory_crud(db, factory_id, name, location, description)
    except ValueError:
        raise FactoryUpdateError("Unable to update factory.")