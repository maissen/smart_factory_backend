from sqlalchemy.orm import Session
from src.helpers.factory import assert_factory_access
from src.models.factory_model import Factory
from src.models.shifts_model import Shift
from src.services.factory.get_factory_service import get_factory_by_id_service

from src.db_crud.shift.get_shift_crud import get_shift_by_factory_id_crud, get_shift_by_id_crud

from src.exceptions.shifts_exceptions import (
    ShiftNotFoundError,
)


def get_shift_by_id_service(db: Session, shift_id: int, current_user) -> Shift:
    """
    Get a shift by ID.
    """
    try:
        shift = get_shift_by_id_crud(db, shift_id)
    except:
        raise ShiftNotFoundError(f"Shift with id {shift_id} is not found.")

    assert_factory_access(shift.factory, current_user)

    return shift


def get_shift_of_factory_service(db: Session, factory_id: int, current_user) -> Shift | None:
    """
    Get the shift belonging to a specific factory.
    """
    factory = get_factory_by_id_service(db=db, factory_id=factory_id)

    assert_factory_access(factory, current_user)

    shift = get_shift_by_factory_id_crud(db, factory_id)

    if not shift:
        raise ShiftNotFoundError(f"This Factory has no shift yet.")

    return shift


def check_if_factory_has_shift_service(db: Session, factory_id: int, current_user) -> bool:
    """
    Check if a given factory has a shift or not without raising error
    """

    try:
        factory = get_shift_of_factory_service(db=db, factory_id=factory_id, current_user=current_user)
    except:
        return False
    
    return True
