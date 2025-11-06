from db_crud.factory.get_factory_crud import get_factory_of_user_crud
from sqlalchemy.orm import Session

from src.models.factory_model import Factory
from src.services.user.get_user_by_id_service import get_user_by_id_service
from src.db_crud.factory import (
    get_factory_by_id_crud,
    get_factories_by_owner_crud,
    get_all_factories_crud,
)
from src.exceptions.factory_exceptions import (
    FactoryNotFoundError,
    InvalidFactoryIdError
)
from src.exceptions.user_exceptions import InvalidUserIdError


def get_factory_by_id_service(db: Session, factory_id: int) -> Factory:

    # ID validation
    if not isinstance(factory_id, int):
        raise InvalidFactoryIdError("Factory ID must be an integer.")

    factory = get_factory_by_id_crud(db, factory_id)
    if not factory:
        raise FactoryNotFoundError(factory_id)
    return factory


def list_factories_service(db: Session, admin: bool, user_id: int = None) -> list[Factory]:
    if admin:
        return get_all_factories_crud(db)
    return get_factories_by_owner_crud(db, user_id)


def get_factory_of_user_service(
    db: Session,
    user_id: int,
    raise_if_empty: bool = False
):
    # Validate user_id
    if not isinstance(user_id, int):
        raise InvalidUserIdError("User ID must be an integer.")

    # Ensure user exists
    user = get_user_by_id_service(db, user_id)


    try:
        factory = get_factory_of_user_crud(db, user_id)
        
    except:
        raise FactoryNotFoundError("User does not have a factory.")

    return factory