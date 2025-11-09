from src.exceptions.user_exceptions import UserAuthorizationError
from src.core.settings import settings

def require_admin(user_role: str):
    if user_role != settings.USER_ALLOWED_ROLES[0]: # admin
        raise UserAuthorizationError()
    return