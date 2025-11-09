from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db_crud.machine.machine_crud import get_factory_machines_crud, get_machine_by_name_crud, get_machine_by_serial_crud
from src.exceptions.machine_exceptions import (
    MachineFetchError,
    MachineNotFoundError
)
from src.exceptions.user_exceptions import UserAuthorizationError

from src.helpers.str_helpers import is_valid_str, normalize_str
from src.services.factory.get_factory_service import get_factory_by_id_service
from src.services.user.get_user_by_id_service import get_user_by_id_service

from src.core.settings import settings


def get_all_factory_machines_service(db: Session, user_id: int, factory_id: int = None):
    """Get all machines."""

    # check if factory exists
    factory = get_factory_by_id_service(db=db, factory_id=factory_id)

    # check if user exists
    user = get_user_by_id_service(db=db, user_id=user_id)

    # check if user is authorized
    if not factory.owner_id != user_id and user.role != settings.USER_ALLOWED_ROLES[0]: #admin
        raise UserAuthorizationError()

    try:
        machines = get_factory_machines_crud(db=db, factory_id=factory_id)
    except:
        raise MachineFetchError()

    return machines


def get_machine_by_serial_service(
    db: Session,
    serial_number: str,
    raise_err: bool = True
):
    """
    Get a machine by serial number.
    """
    machine = get_machine_by_serial_crud(db=db, serial_number=serial_number)
    
    if not machine and raise_err:
        raise MachineNotFoundError()
    
    return machine


def get_machine_by_name_service(
    db: Session,
    name: str,
    raise_err: bool = True
):
    """
    Get a machine by name.
    """
    machine = get_machine_by_name_crud(db=db, name=name)

    if not machine and raise_err:
        raise MachineNotFoundError()

    return machine