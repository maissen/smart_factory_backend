class UserError(Exception):
    """Base exception for all user-related errors."""
    def __init__(self, message=None):
        if message is None:
            message = "An unknown user error occurred."
        super().__init__(message)


# ============================================
# Resource Not Found Errors (404)
# ============================================

class UserNotFoundError(UserError):
    """Raised when a user cannot be found."""
    def __init__(self, message=None):
        if message is None:
            message = "User could not be found."
        super().__init__(message)


class EmailDoesNotExistError(UserError):
    """Raised when an email does not exist in the system."""
    def __init__(self, message=None):
        if message is None:
            message = "Email does not exist."
        super().__init__(message)


class PhoneNumberDoesNotExistError(UserError):
    """Raised when a phone number does not exist in the system."""
    def __init__(self, message=None):
        if message is None:
            message = "Phone number does not exist."
        super().__init__(message)


# ============================================
# Validation Errors (400)
# ============================================

class UserValidationError(UserError):
    """Raised for invalid user input or validation failure."""
    def __init__(self, message=None):
        if message is None:
            message = "Invalid user input."
        super().__init__(message)


class InvalidUserIdError(UserValidationError):
    """Raised when the user ID is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "User ID must be a positive integer."
        super().__init__(message)


class InvalidFullNameError(UserValidationError):
    """Raised when the full name is empty or invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Full name is empty or invalid."
        super().__init__(message)


class InvalidEmailError(UserValidationError):
    """Raised when the email format is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Email format is invalid or empty."
        super().__init__(message)


class InvalidPasswordError(UserValidationError):
    """Raised when the password does not meet requirements."""
    def __init__(self, message=None):
        if message is None:
            message = "Password does not meet security requirements."
        super().__init__(message)


class InvalidPhoneNumberError(UserValidationError):
    """Raised when the phone number format is invalid."""
    def __init__(self, message=None):
        if message is None:
            message = "Phone number format is invalid."
        super().__init__(message)


class InvalidRoleError(UserValidationError):
    """Raised when the role is invalid or non-existent."""
    def __init__(self, message=None):
        if message is None:
            message = "Role is invalid or does not exist."
        super().__init__(message)


class EmptyRoleError(UserValidationError):
    """Raised when the role field is empty."""
    def __init__(self, message=None):
        if message is None:
            message = "Role cannot be empty."
        super().__init__(message)


# ============================================
# Conflict Errors (409)
# ============================================

class UserConflictError(UserError):
    """Raised when there is a resource conflict."""
    def __init__(self, message=None):
        if message is None:
            message = "Resource conflict error."
        super().__init__(message)


class EmailAlreadyExistsError(UserConflictError):
    """Raised when the email already exists in the system."""
    def __init__(self, message=None):
        if message is None:
            message = "Email already exists."
        super().__init__(message)


class PhoneNumberAlreadyExistsError(UserConflictError):
    """Raised when the phone number already exists in the system."""
    def __init__(self, message=None):
        if message is None:
            message = "Phone number already exists."
        super().__init__(message)


# ============================================
# Authentication/Authorization Errors (401/403)
# ============================================

class UserAuthenticationError(UserError):
    """Raised when authentication fails."""
    def __init__(self, message=None):
        if message is None:
            message = "Authentication failed."
        super().__init__(message)


class IncorrectPasswordError(UserAuthenticationError):
    """Raised when the provided password is incorrect."""
    def __init__(self, message=None):
        if message is None:
            message = "Incorrect password."
        super().__init__(message)


class UserAuthorizationError(UserError):
    """Raised when the user is not authorized for an action."""
    def __init__(self, message=None):
        if message is None:
            message = "User is not authorized."
        super().__init__(message)


class MissingPasswordError(UserValidationError):
    """Raised when the password is missing."""
    def __init__(self, message=None):
        if message is None:
            message = "Password is missing."
        super().__init__(message)


# ============================================
# Internal/Operational Errors (500)
# ============================================

class UserOperationError(UserError):
    """Raised for internal errors during user operations."""
    def __init__(self, message=None):
        if message is None:
            message = "An internal user operation error occurred."
        super().__init__(message)


class UserCreationError(UserOperationError):
    """Raised when creating a user fails internally."""
    def __init__(self, message=None):
        if message is None:
            message = "User creation failed due to internal error."
        super().__init__(message)


class UserUpdateError(UserOperationError):
    """Raised when updating a user fails internally."""
    def __init__(self, message=None):
        if message is None:
            message = "User update failed due to internal error."
        super().__init__(message)


class UserDeletionError(UserOperationError):
    """Raised when deleting a user fails internally."""
    def __init__(self, message=None):
        if message is None:
            message = "User deletion failed due to internal error."
        super().__init__(message)


class UserFetchError(UserOperationError):
    """Raised when fetching users fails internally."""
    def __init__(self, message=None):
        if message is None:
            message = "Fetching user(s) failed due to internal error."
        super().__init__(message)


class PasswordUpdateError(UserOperationError):
    """Raised when updating a password fails internally."""
    def __init__(self, message=None):
        if message is None:
            message = "Password update failed due to internal error."
        super().__init__(message)


# ============================================
# Authorization Errors (403)
# ============================================

class UserNotAllowedError(UserError):
    """Raised when the user is not allowed to perform an action."""
    def __init__(self, message=None):
        if message is None:
            message = "User is not allowed to perform this action."
        super().__init__(message)
