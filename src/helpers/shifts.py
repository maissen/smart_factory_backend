from datetime import time
from src.exceptions.shifts_exceptions import (
    ShiftTimeRangeError,
)


def validate_time_range(start_time: time, end_time: time):
    """
    Ensure time range is valid (simple rule).
    """
    if start_time >= end_time:
        raise ShiftTimeRangeError("End time must be greater than start time.")