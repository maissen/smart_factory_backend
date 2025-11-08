class MachineError(Exception):
    """Base class for all machine-related errors."""
    def __init__(self, message=None):
        if message is None:
            message = "An unknown machine error occurred."
        super().__init__(message)


class MachineNotFoundError(MachineError):
    """Raised when a machine cannot be found by ID."""
    def __init__(self, message=None):
        if message is None:
            message = "Machine could not be found."
        super().__init__(message)


class MachineNameAlreadyExistsError(MachineError):
    """Raised when creating/updating a machine with a name that already exists."""
    def __init__(self, message=None):
        if message is None:
            message = "Machine name already exists."
        super().__init__(message)


class MachineSerialNumberAlreadyExistsError(MachineError):
    """Raised when creating/updating a machine with a serial number that already exists."""
    def __init__(self, message=None):
        if message is None:
            message = "Machine serial number already exists."
        super().__init__(message)


class InvalidMachineStatusError(MachineError):
    """Raised when setting an invalid status."""
    def __init__(self, message=None):
        if message is None:
            message = "Invalid machine status."
        super().__init__(message)


class MachineAccessDeniedError(MachineError):
    """
    Raised when a client tries to interact with a machine belonging to another factory.
    Used only if your auth rules require client isolation.
    """
    def __init__(self, message=None):
        if message is None:
            message = "Access to this machine is denied."
        super().__init__(message)


class MachineFetchError(MachineError):
    """
    Raised when an error occurs while fetching the machine from the database.
    """
    def __init__(self, message=None):
        if message is None:
            message = "Failed to fetch machine from the database."
        super().__init__(message)


class MachineInvalidNameError(MachineError):
    """Raised when the machine's name is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Machine name is invalid."
        super().__init__(message)


class MachineInvalidSerialNumberError(MachineError):
    """Raised when the machine's serial number is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Machine serial number is invalid."
        super().__init__(message)
