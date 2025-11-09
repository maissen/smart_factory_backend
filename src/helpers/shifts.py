from datetime import time
from src.exceptions.shifts_exceptions import *


def validate_time_range(start_time: time, end_time: time):
    """
    Ensure time range is valid.
    """
    # Validate time input
    if not isinstance(start_time, time):
        raise ShiftStartTimeIsInvalidError()

    if not isinstance(end_time, time):
        raise ShiftEndTimeIsInvalidError()
    
    if start_time >= end_time:
        raise ShiftTimeRangeError()
    
from src.exceptions.shifts_exceptions import ShiftError

def validate_shift_id(shift_id: int):
    if not isinstance(shift_id, int) or shift_id <= 0:
        raise ShiftError("Invalid shift id.")