from sqlalchemy.orm import Session
from datetime import time
from src.helpers.factory import assert_factory_access
from src.helpers.shifts import validate_time_range

from src.models.factory_model import Factory
from src.models.shifts_model import Shift

from src.db_crud.shift.create_shift_crud import create_shift_crud
from src.db_crud.shift.get_shift_crud import get_shift_by_factory_id_crud
from src.services.shifts.get_shift_service import check_if_factory_has_shift_service

from src.exceptions.shifts_exceptions import (
    ShiftNotFoundError,
    ShiftAlreadyExistsError,
)


def create_shift_service(
    db: Session,
    factory_id: int,
    name: str,
    start_time: time,
    end_time: time,
    current_user,
) -> Shift:
    """
    Create a shift for a factory.
    """
    factory = db.query(Factory).filter(Factory.id == factory_id).first()
    if factory is None:
        raise ShiftNotFoundError(factory_id)

    assert_factory_access(factory, current_user)

    existing = check_if_factory_has_shift_service(db=db, factory_id=factory_id, current_user=current_user)
    if existing:
        raise ShiftAlreadyExistsError("Factory already has a shift.")

    validate_time_range(start_time, end_time)

    return create_shift_crud(db, factory_id, name, start_time, end_time)
