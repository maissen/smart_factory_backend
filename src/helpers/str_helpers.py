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
    if not isinstance(value, str):
        raise ValueError("Expected a string")

    # strip() removes leading and trailing spaces
    # split() splits on any whitespace sequence
    # join() joins with a single space
    return " ".join(value.strip().split())
