class FactoryError(Exception):
    """Base class for all factory-related errors."""


class FactoryNotFoundError(FactoryError):
    """Raised when a requested factory does not exist."""
    pass


class FactoryOwnerNotFoundError(FactoryError):
    """Raised when the provided owner_id does not match any user."""
    pass


class FactoryAlreadyExistsError(FactoryError):
    """Raised when a factory conflicts with existing records (e.g., same name/location)."""
    pass


class FactoryUpdateError(FactoryError):
    """Raised when factory update fails due to DB constraint or ownership invalidation."""
    pass


class FactoryDeleteError(FactoryError):
    """Raised when deleting a factory fails."""
    pass


class FactoryPermissionError(FactoryError):
    """Raised when user does not have permission to modify this factory."""
    pass
