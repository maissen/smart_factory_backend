class MachineLogError(Exception):
    """Base class for all machine log-related errors."""
    def __init__(self, message=None):
        if message is None:
            message = "An unknown machine log error occurred."
        super().__init__(message)


class MachineLogNotFoundError(MachineLogError):
    """Raised when a machine log cannot be found by ID."""
    def __init__(self, message=None):
        if message is None:
            message = "Machine log could not be found."
        super().__init__(message)


class InvalidMachineLogStatusError(MachineLogError):
    """Raised when setting an invalid status for a machine log."""
    def __init__(self, message=None):
        if message is None:
            message = "Invalid machine log status."
        super().__init__(message)


class MachineLogAccessDeniedError(MachineLogError):
    """
    Raised when a client tries to access logs of a machine belonging to another factory.
    Used only if your auth rules require client isolation.
    """
    def __init__(self, message=None):
        if message is None:
            message = "Access to this machine log is denied."
        super().__init__(message)


class MachineLogCreateError(MachineLogError):
    """Raised when creating a machine log fails."""
    def __init__(self, message=None):
        if message is None:
            message = "Failed to create machine log."
        super().__init__(message)


class MachineLogDeleteError(MachineLogError):
    """Raised when deleting machine logs fails."""
    def __init__(self, message=None):
        if message is None:
            message = "Failed to delete machine logs."
        super().__init__(message)


class MachineLogFetchError(MachineLogError):
    """Raised when fetching machine logs from the database fails."""
    def __init__(self, message=None):
        if message is None:
            message = "Failed to fetch machine logs from the database."
        super().__init__(message)
