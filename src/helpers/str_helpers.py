import re
from src.exceptions.user_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidPhoneNumberError,
    InvalidFullNameError
)



DEFAULT_ERROR_MESSAGE = "error message must be passed"


def is_valid_str(value: str) -> bool:
    """
    Returns True if the given string is not None, not empty,
    and not just whitespace.
    """
    return isinstance(value, str) and value.strip() != ""


def normalize_str(value: str, error_msg: str = None) -> str:
    """
    Cleans a string by:
    - Stripping leading & trailing spaces
    - Converting multiple spaces to a single space

    Raises:
        InvalidFullNameError: If string is invalid.
    """
    error_msg = error_msg or DEFAULT_ERROR_MESSAGE

    if not is_valid_str(value):
        raise InvalidFullNameError(error_msg)

    return " ".join(value.strip().split())


def validate_email(email: str, error_msg: str = None) -> str:
    """
    Validate email format using a basic regex.
    Raises:
        InvalidEmailError
    """
    error_msg = error_msg or DEFAULT_ERROR_MESSAGE

    if not email or not isinstance(email, str):
        raise InvalidEmailError(error_msg)

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise InvalidEmailError(error_msg)

    return email


def validate_password(password: str, error_msg: str = None) -> str:
    """
    Validate password meets security requirements.
    Raises:
        InvalidPasswordError
    """
    error_msg = error_msg or DEFAULT_ERROR_MESSAGE

    if not password or not isinstance(password, str):
        raise InvalidPasswordError(error_msg)

    if len(password) < 6:
        raise InvalidPasswordError(error_msg)

    return password


def validate_phone_number(phone_number: str, error_msg: str = None) -> str:
    """
    Validate phone number and return digits-only version.
    Raises:
        InvalidPhoneNumberError
    """
    error_msg = error_msg or DEFAULT_ERROR_MESSAGE

    if not phone_number or not isinstance(phone_number, str):
        raise InvalidPhoneNumberError(error_msg)

    cleaned = re.sub(r"\D", "", phone_number)

    if len(cleaned) < 8:
        raise InvalidPhoneNumberError(error_msg)

    return cleaned
