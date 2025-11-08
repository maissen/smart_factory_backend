class ShiftError(Exception):
    """Base class for all shift-related exceptions."""
    pass


class ShiftNotFoundError(ShiftError):
    """Raised when a shift is not found."""
    def __init__(self, shift_id: int):
        super().__init__(f"Shift with id '{shift_id}' was not found.")


class ShiftAlreadyExistsError(ShiftError):
    """Raised when trying to create a shift for a factory that already has one."""
    def __init__(self, factory_id: int):
        super().__init__(f"Factory already has a shift. Only one shift is allowed per factory.")


class ShiftPermissionError(ShiftError):
    """Raised when a user attempts an action they are not allowed to perform."""
    def __init__(self):
        super().__init__("You do not have permission to perform this action on this shift.")


class ShiftTimeRangeError(ShiftError):
    """Raised when the shift start time is later than the end time."""
    def __init__(self):
        super().__init__(f"Invalid shift time range.")
