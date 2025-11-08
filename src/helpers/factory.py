from src.models.factory_model import Factory
from src.core.settings import settings

from src.exceptions.shifts_exceptions import (
    ShiftPermissionError,
)

def assert_factory_access(factory: Factory, current_user):
    """
    Ensure user can modify or view this factory's shift.
    """
    if current_user.role == settings.USER_ALLOWED_ROLES[0]: # admin
        return

    if current_user.role == settings.USER_ALLOWED_ROLES[1] and factory.owner_id == current_user.id:
        return

    raise ShiftPermissionError()