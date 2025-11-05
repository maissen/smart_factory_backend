def is_valid_str(value: str) -> bool:
    """
    Returns True if the given string is not None, not empty,
    and not just whitespace.
    """

    return isinstance(value, str) and value.strip() != ""


def normalize_str(value: str) -> str:
    """
    Cleans a string by:
    - Stripping leading & trailing spaces
    - Converting multiple spaces inside the string to a single space
    """

    # strip() removes leading and trailing spaces
    # split() splits on any whitespace sequence
    # join() joins with a single space
    return " ".join(value.strip().split())


import re


def validate_email(email: str):
    """Validate email format using basic regex pattern."""

    if not email or not isinstance(email, str):
        raise ValueError("Email is required")

    # Simple email regex
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    if not re.match(pattern, email):
        raise ValueError("Invalid email format")

    return email


def validate_password(password: str):
    """Validate password meets minimum length requirement."""

    if not password or not isinstance(password, str):
        raise ValueError("Password is required")

    if len(password) < 6:
        raise ValueError("Password must be at least 6 characters long")

    # Later: add uppercase, numbers, special chars rules if desired
    return password


def validate_phone_number(phone_number: str):
    """Validate phone number and return digits-only version."""
    if not phone_number or not isinstance(phone_number, str):
        raise ValueError("Phone number is required")

    # Keep it simple: digits only + length >= 8
    cleaned = re.sub(r"\D", "", phone_number)  # remove spaces/dashes
    if len(cleaned) < 8:
        raise ValueError("Phone number must contain at least 8 digits")

    return cleaned