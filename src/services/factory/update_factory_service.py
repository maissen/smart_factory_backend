from sqlalchemy.orm import Session

from src.models.factory_model import Factory
from src.db_crud.factory.update_factory_crud import update_factory_crud
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.exceptions.factory_exceptions import (
    FactoryPermissionError,
    FactoryUpdateError,
)

from src.helpers.validate_user_id import validate_user_id
from src.helpers.str_helpers import *

def update_factory_service(
    db: Session,
    user_id: int,
    name: str,
    location: str,
    description: str,
) -> Factory:
    
    validate_user_id(user_id)

    is_valid_str(name, raise_on_error=True, err_msg="Factory name must be a non-empty valid string.")
    is_valid_str(location, raise_on_error=True, err_msg="Factory location must be a non-empty valid string.")
    is_valid_str(description, raise_on_error=True, err_msg="Factory description must be a non-empty valid string.")
    
    factory = get_factory_of_user_service(db=db, user_id=user_id)

    try:
        return update_factory_crud(db, factory.id, name, location, description)
    except:
        raise FactoryUpdateError("An error occured while updating factory.")