import re
from src.exceptions.user_exceptions import (
    InvalidEmailError,
    InvalidPasswordError,
    InvalidPhoneNumberError,
    InvalidFullNameError
)



DEFAULT_ERROR_MESSAGE = "error message must be passed"
MIN_PASSWORD_LENGTH = 8
MIN_PHONE_NUMBER_LENGTH = 8


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


def validate_email(email: str) -> str:
    """
    Validate email format using a basic regex.
    Raises:
        InvalidEmailError
    """

    if not email or not isinstance(email, str):
        raise InvalidEmailError("The email must be a string")

    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise InvalidEmailError("The email is invalid")

    return email


def validate_password(password: str) -> str:
    """
    Validate password meets security requirements.
    Raises:
        InvalidPasswordError
    """

    if not password or not isinstance(password, str):
        raise InvalidPasswordError("Password must be a string")

    if len(password) < 6:
        raise InvalidPasswordError(f"Password length must be at least {MIN_PASSWORD_LENGTH} caracters")

    return password


def validate_phone_number(phone_number: str) -> str:
    """
    Validate phone number and return digits-only version.
    Raises:
        InvalidPhoneNumberError
    """

    if not is_valid_str(phone_number):
        raise InvalidPhoneNumberError("The phone number must be a string")

    cleaned = re.sub(r"\D", "", phone_number)

    if len(cleaned) < 8:
        raise InvalidPhoneNumberError(f"Phone number length must be {MIN_PHONE_NUMBER_LENGTH}")

    return cleaned
