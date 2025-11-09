from sqlalchemy.orm import Session
from datetime import time
from src.helpers.factory import assert_factory_access
from src.helpers.shifts import validate_time_range

from src.models.factory_model import Factory
from src.models.shifts_model import Shift

from src.db_crud.shift.create_shift_crud import create_shift_crud
from src.services.shifts.get_shift_service import get_shift_of_factory_service
from src.helpers.str_helpers import is_valid_str
from src.services.factory.get_factory_service import get_factory_by_owner_crud

from src.exceptions.shifts_exceptions import *

def create_shift_service(
    db: Session,
    name: str,
    start_time: time,
    end_time: time,
    user_id: int,
) -> Shift:
    """
    Create a shift for a factory.
    """

    is_valid_str(name, raise_on_error=True, err_msg="Shift name must be a valid non-empty string.")
    validate_time_range(start_time, end_time)

    # ensure user has a factory
    factory = get_factory_by_owner_crud(db=db, user_id=user_id)

    existing_shift = get_shift_of_factory_service(db=db, factory_id=factory.id, raise_error=False)
    if existing_shift:
        raise ShiftAlreadyExistsError()

    try:
        new_shift = create_shift_crud(db, factory.id, name, start_time, end_time)
        return new_shift
    except Exception as e:
        print(e)
        raise ShiftError("Failed to create a new shift.")

