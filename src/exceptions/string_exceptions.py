class InvalidStringError(Exception):
    """Raised when a string is invalid."""
    def __init__(self, message="String is invalid."):
        super().__init__(message)