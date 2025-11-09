from src.exceptions.user_exceptions import InvalidUserIdError

def validate_user_id(user_id: int):
    if not isinstance(user_id, int) or user_id <= 0:
        raise InvalidUserIdError()