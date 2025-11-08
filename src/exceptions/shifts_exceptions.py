class ShiftError(Exception):
    """Base class for all shift-related exceptions."""
    def __init__(self, message=None):
        if message is None:
            message = "An unknown shift error occurred."
        super().__init__(message)


class ShiftNotFoundError(ShiftError):
    """Raised when a shift is not found."""
    def __init__(self, message=None):
        if message is None:
            message = "Shift could not be found."
        super().__init__(message)


class ShiftAlreadyExistsError(ShiftError):
    """Raised when trying to create a shift for a factory that already has one."""
    def __init__(self, message=None):
        if message is None:
            message = "Shift already exists for this factory."
        super().__init__(message)


class ShiftPermissionError(ShiftError):
    """Raised when a user attempts an action they are not allowed to perform."""
    def __init__(self, message=None):
        if message is None:
            message = "You do not have permission to perform this action on the shift."
        super().__init__(message)


class ShiftTimeRangeError(ShiftError):
    """Raised when the shift start time is later than the end time."""
    def __init__(self, message=None):
        if message is None:
            message = "Shift start time cannot be later than the end time."
        super().__init__(message)


class ShiftNameIsInvalidError(ShiftError):
    """Raised when shift's name is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Shift name is invalid."
        super().__init__(message)


class ShiftStartTimeIsInvalidError(ShiftError):
    """Raised when shift's start time is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Shift start time is invalid."
        super().__init__(message)


class ShiftEndTimeIsInvalidError(ShiftError):
    """Raised when shift's end time is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Shift end time is invalid."
        super().__init__(message)
