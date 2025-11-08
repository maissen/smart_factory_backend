from datetime import time
from src.helpers.factory import assert_factory_access
from src.helpers.shifts import validate_time_range
from sqlalchemy.orm import Session

from src.models.shifts_model import Shift
from src.services.shifts.get_shift_service import get_shift_by_id_service
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.helpers.str_helpers import is_valid_str

from src.db_crud.shift.update_shift_crud import update_shift_crud
from src.helpers.factory import assert_factory_access
from src.exceptions.shifts_exceptions import (
    ShiftEndTimeIsInvalidError,
    ShiftNameIsInvalidError,
    ShiftStartTimeIsInvalidError,
)


def update_shift_service(
    db: Session,
    shift_id: int,
    current_user,
    name: str,
    start_time: str,
    end_time: str
) -> Shift:
    """
    Update shift attributes.
    """
    # Validate input
    if not is_valid_str(name):
        raise ShiftNameIsInvalidError()
    
    # Validate time input
    if not isinstance(start_time, time):
        raise ShiftStartTimeIsInvalidError()

    if not isinstance(end_time, time):
        raise ShiftEndTimeIsInvalidError()

    # Fetch the shift and factory
    shift = get_shift_by_id_service(db=db, shift_id=shift_id, current_user=current_user)
    factory = get_factory_of_user_service(db=db, user_id=current_user.id)

    # Check permissions
    assert_factory_access(factory=factory, current_user=current_user)

    # Validate time range
    validate_time_range(start_time=start_time, end_time=end_time)

    # Update the shift
    return update_shift_crud(db, shift_id, start_time=start_time, end_time=end_time, name=name)
