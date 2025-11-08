class MachineError(Exception):
    """Base class for all machine-related errors."""


class MachineNotFoundError(MachineError):
    """Raised when a machine cannot be found by ID."""
    pass

class MachineNameAlreadyExistsError(MachineError):
    """Raised when creating/updating a machine with a name that already exists."""
    pass

class MachineSerialNumberAlreadyExistsError(MachineError):
    """Raised when creating/updating a machine with a serial number that already exists."""
    pass

class InvalidMachineStatusError(MachineError):
    """Raised when setting an invalid status."""
    pass


class MachineAccessDeniedError(MachineError):
    """
    Raised when a client tries to interact with a machine belonging to another factory.
    Used only if your auth rules require client isolation.
    """
    pass