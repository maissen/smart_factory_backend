class TokenError(Exception):
    """Base class for all token-related exceptions."""
    pass


class TokenExpiredError(TokenError):
    """Raised when a JWT token has expired."""
    def __init__(self, message="Token has expired"):
        super().__init__(message)


class InvalidTokenError(TokenError):
    """Raised when a JWT token is invalid."""
    def __init__(self, message="Invalid token"):
        super().__init__(message)
