from src.helpers.factory import assert_factory_access
from src.helpers.shifts import validate_time_range
from sqlalchemy.orm import Session

from src.models.shifts_model import Shift
from src.services.shifts.get_shift_service import get_shift_by_id_service

from src.db_crud.shift.update_shift_crud import update_shift_crud
from src.exceptions.shifts_exceptions import (
    ShiftNotFoundError,
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
    try:
        shift = get_shift_by_id_service(db=db, shift_id=shift_id, current_user=current_user)

    except ShiftNotFoundError as e:
        raise ShiftNotFoundError(e)

    except:
        raise ShiftNotFoundError(shift_id)

    validate_time_range(start_time=start_time, end_time=end_time)

    return update_shift_crud(db, shift_id, start_time=start_time, end_time=end_time, name=name)

