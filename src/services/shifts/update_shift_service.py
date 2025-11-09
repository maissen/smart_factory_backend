from datetime import time
from src.helpers.shifts import validate_time_range
from sqlalchemy.orm import Session

from src.models.shifts_model import Shift
from src.services.shifts.get_shift_service import get_shift_of_factory_service
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.helpers.str_helpers import is_valid_str
from src.helpers.str_helpers import is_valid_str

from src.db_crud.shift.update_shift_crud import update_shift_crud
from src.exceptions.shifts_exceptions import (
    ShiftError
)


def update_shift_service(
    db: Session,
    user_id: int,
    name: str,
    start_time: str,
    end_time: str
) -> Shift:
    """
    Update shift attributes.
    """
    # Validate input
    is_valid_str(name, raise_on_error=True, err_msg="Shift name must be a non-empty string.")
    
    validate_time_range(start_time=start_time, end_time=end_time)

    # Ensure factory exists
    factory = get_factory_of_user_service(db=db, user_id=user_id)

    # ensure shift exists
    shift = get_shift_of_factory_service(db=db, factory_id=factory.id)

    # Update the shift
    try:
        return update_shift_crud(db, shift.id, start_time=start_time, end_time=end_time, name=name)
    except Exception as e:
        print(e)
        raise ShiftError("Failed to update shift.")
