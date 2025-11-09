from sqlalchemy.orm import Session

from src.models.factory_model import Factory
from src.services.user.get_user_by_id_service import get_user_by_id_service
from src.db_crud.factory.get_factory_crud import (
    get_factory_by_id_crud,
    get_factory_by_owner_crud,
    get_all_factories_crud,
)
from src.exceptions.factory_exceptions import *
from src.helpers.validate_user_id import validate_user_id
from src.helpers.factory import validate_factory_id


def get_factory_by_id_service(db: Session, factory_id: int) -> Factory:

    # ID validation
    validate_factory_id(factory_id)

    try:
        factory = get_factory_by_id_crud(db, factory_id)
        if not factory:
            raise FactoryNotFoundError()
        
        return factory
    
    except Exception as e:
        raise FactoryError("Failed to fetch factories.")


def list_factories_service(db: Session) -> list[Factory]:
    try:
        return get_all_factories_crud(db)
    except:
        raise FactoryError("An error occured while fetching factories.")


def get_factory_of_user_service(
    db: Session,
    user_id: int,
    raise_error: bool = True
):
    # Validate user_id
    validate_user_id(user_id)

    # Ensure user exists
    user = get_user_by_id_service(db, user_id)

    factory = get_factory_by_owner_crud(db, user_id)
    if not factory:
        if raise_error:
            raise FactoryNotFoundError("You don't have a factory yet.")
        return None

    return factory