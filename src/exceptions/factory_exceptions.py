class FactoryError(Exception):
    """Base class for all factory-related errors."""
    def __init__(self, message=None):
        if message is None:
            message = "An error occurred in the factory module."
        super().__init__(message)


class FactoryNotFoundError(FactoryError):
    """Raised when a requested factory does not exist."""
    def __init__(self, message=None):
        if message is None:
            message = "The requested factory does not exist."
        super().__init__(message)


class FactoryOwnerNotFoundError(FactoryError):
    """Raised when the provided owner_id does not match any user."""
    def __init__(self, message=None):
        if message is None:
            message = "No user found with the given owner ID."
        super().__init__(message)


class FactoryAlreadyExistsError(FactoryError):
    """Raised when a factory conflicts with existing records (e.g., same name/location)."""
    def __init__(self, message=None):
        if message is None:
            message = "A factory with the same name already exists."
        super().__init__(message)


class FactoryUpdateError(FactoryError):
    """Raised when factory update fails due to DB constraint or ownership invalidation."""
    def __init__(self, message=None):
        if message is None:
            message = "Failed to update the factory due to constraints or invalid ownership."
        super().__init__(message)


class FactoryDeleteError(FactoryError):
    """Raised when deleting a factory fails."""
    def __init__(self, message=None):
        if message is None:
            message = "Failed to delete the factory."
        super().__init__(message)


class FactoryPermissionError(FactoryError):
    """Raised when user does not have permission to access this factory."""
    def __init__(self, message=None):
        if message is None:
            message = "You do not have permission to access this factory."
        super().__init__(message)


class InvalidFactoryIdError(FactoryError):
    """Raised when the factory id is invalid"""
    def __init__(self, message=None):
        if message is None:
            message = "The provided factory ID is invalid."
        super().__init__(message)
