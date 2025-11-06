class UserError(Exception):
    """
    Base exception for all user-related errors.
    All user service exceptions should inherit from this.
    """
    pass


# ============================================
# Resource Not Found Errors (404)
# ============================================

class UserNotFoundError(UserError):
    """
    Raised when a user cannot be found by the specified identifier.
    Maps to: HTTP 404
    """
    pass


class EmailDoesNotExistError(UserError):
    """
    Raised when a user lookup fails because the specified email does not exist.
    Maps to: HTTP 404
    """
    pass


class PhoneNumberDoesNotExistError(UserError):
    """
    Raised when a user lookup fails because the specified phone number does not exist.
    Maps to: HTTP 404
    """
    pass



# ============================================
# Validation Errors (400)
# ============================================

class UserValidationError(UserError):
    """
    Base class for all input validation errors.
    Maps to: HTTP 400
    """
    pass


class InvalidUserIdError(UserValidationError):
    """
    Raised when user_id is not a positive integer.
    """
    pass


class InvalidFullNameError(UserValidationError):
    """
    Raised when full_name is empty or invalid.
    """
    pass


class InvalidEmailError(UserValidationError):
    """
    Raised when email format is invalid or empty.
    """
    pass


class InvalidPasswordError(UserValidationError):
    """
    Raised when password doesn't meet security requirements.
    """
    pass


class InvalidPhoneNumberError(UserValidationError):
    """
    Raised when phone number format is invalid.
    """
    pass


class InvalidRoleError(UserValidationError):
    """
    Raised when role is invalid or doesn't exist.
    """
    pass


class EmptyRoleError(UserValidationError):
    """
    Raised when role is an empty string.
    """
    pass


# ============================================
# Conflict Errors (409)
# ============================================

class UserConflictError(UserError):
    """
    Base class for resource conflict errors.
    Maps to: HTTP 409
    """
    pass


class EmailAlreadyExistsError(UserConflictError):
    """
    Raised when attempting to create/update a user with an email that already exists.
    """
    pass


class PhoneNumberAlreadyExistsError(UserConflictError):
    """
    Raised when attempting to create/update a user with a phone number that already exists.
    """
    pass


# ============================================
# Authentication/Authorization Errors (401/403)
# ============================================

class UserAuthenticationError(UserError):
    """
    Base class for authentication-related errors.
    Maps to: HTTP 401
    """
    pass


class IncorrectPasswordError(UserAuthenticationError):
    """
    Raised when old password doesn't match during password update.
    """
    pass


class MissingPasswordError(UserValidationError):
    """
    Raised when old password is not provided during password update.
    """
    pass


# ============================================
# Internal/Operational Errors (500)
# ============================================

class UserOperationError(UserError):
    """
    Raised when an unexpected internal error occurs during user operations.
    This typically indicates a database failure or unexpected system error.
    Maps to: HTTP 500
    """
    pass


class UserCreationError(UserOperationError):
    """
    Raised when user creation fails due to internal errors.
    """
    pass


class UserUpdateError(UserOperationError):
    """
    Raised when user update fails due to internal errors.
    """
    pass


class UserDeletionError(UserOperationError):
    """
    Raised when user deletion fails due to internal errors.
    """
    pass


class UserFetchError(UserOperationError):
    """
    Raised when fetching user(s) fails due to internal errors.
    """
    pass


class PasswordUpdateError(UserOperationError):
    """
    Raised when password update fails due to internal errors.
    """
    pass


# ============================================
# Authorization Errors (403)
# ============================================

class UserNotAllowedError(UserError):
    """
    Raised when a user is not allowed to perform an action.
    Maps to: HTTP 403
    """
    pass