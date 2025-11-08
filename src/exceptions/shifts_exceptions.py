class ShiftError(Exception):
    """Base class for all shift-related exceptions."""
    pass


class ShiftNotFoundError(ShiftError):
    """Raised when a shift is not found."""
    pass


class ShiftAlreadyExistsError(ShiftError):
    """Raised when trying to create a shift for a factory that already has one."""
    pass


class ShiftPermissionError(ShiftError):
    """Raised when a user attempts an action they are not allowed to perform."""
    pass


class ShiftTimeRangeError(ShiftError):
    """Raised when the shift start time is later than the end time."""
    pass
