from sqlalchemy.orm import Session

from src.models.factory_model import Factory
from src.db_crud.factory.update_factory_crud import update_factory_crud
from src.services.factory.get_factory_service import get_factory_by_id_service
from src.exceptions.factory_exceptions import (
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
    
    # factory = get_factory_by_id_crud(db, factory_id)
    factory = get_factory_by_id_service(db=db, factory_id=factory_id)

    # Permission check
    if factory.owner_id != user_id:
        raise FactoryPermissionError()

    try:
        return update_factory_crud(db, factory_id, name, location, description)
    except ValueError:
        raise FactoryUpdateError()