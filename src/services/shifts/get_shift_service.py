from sqlalchemy.orm import Session
from src.models.shifts_model import Shift
from src.services.factory.get_factory_service import get_factory_by_id_service
from src.helpers.factory import validate_factory_id

from src.db_crud.shift.get_shift_crud import get_shift_by_factory_id_crud, get_shift_by_id_crud
from src.helpers.shifts import validate_shift_id

from src.exceptions.shifts_exceptions import (
    ShiftNotFoundError,
    ShiftError
)


def get_shift_by_id_service(db: Session, shift_id: int, raise_error: bool = True) -> Shift | None:
    """
    Get a shift by ID.
    """

    validate_shift_id(shift_id)

    try:
        shift = get_shift_by_id_crud(db, shift_id)
    except:
        if raise_error:
            raise ShiftNotFoundError()
        
        return None

    return shift


def get_shift_of_factory_service(db: Session, factory_id: int, raise_error: bool = True) -> Shift | None:
    """
    Get the shift belonging to a specific factory.
    """

    validate_factory_id(factory_id)

    # ensure factory existance
    factory = get_factory_by_id_service(db=db, factory_id=factory_id)

    try:
        shift = get_shift_by_factory_id_crud(db, factory_id)
        if not shift:
            if raise_error:
                raise ShiftNotFoundError()
            
            return None
        
        return shift
        
    except Exception as e:
        print(e)
        raise ShiftError("Failed to fetch shift.")
