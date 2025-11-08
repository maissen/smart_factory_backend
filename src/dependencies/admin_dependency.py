from src.models.user_model import User
from fastapi import Depends
from .get_current_user_dependency import get_current_user
from src.exceptions.user_exceptions import UserAuthorizationError
from src.core.settings import settings

def require_admin(user: User = Depends(get_current_user)):
    if user.role != settings.USER_ALLOWED_ROLES[0]: # admin
        raise UserAuthorizationError()
    return user