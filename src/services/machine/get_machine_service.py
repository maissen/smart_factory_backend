from sqlalchemy.orm import Session

from src.db_crud.machine.machine_crud import get_factory_machines_crud, get_machine_by_id_crud, get_machine_by_name_crud, get_machine_by_serial_crud
from src.exceptions.machine_exceptions import (
    MachineFetchError,
    MachineNotFoundError
)
from src.services.factory.get_factory_service import get_factory_by_id_service
from src.services.user.get_user_by_id_service import get_user_by_id_service
from src.helpers.factory import validate_factory_id
from src.helpers.validate_user_id import validate_user_id

from src.core.settings import settings


def get_all_factory_machines_service(db: Session, user_id: int, factory_id: int = None):
    """Get all machines."""

    validate_user_id(user_id)
    validate_factory_id(factory_id)

    # check if factory exists
    factory = get_factory_by_id_service(db=db, factory_id=factory_id)

    # check if user exists
    user = get_user_by_id_service(db=db, user_id=user_id)

    try:
        machines = get_factory_machines_crud(db=db, factory_id=factory_id)
    except:
        raise MachineFetchError("Failed to fetch machines of the factory.")

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


def get_machine_by_id_service(
    db: Session,
    machine_id: int,
    raise_err: bool = True
):
    """
    Get machine by ID.
    """
    machine = get_machine_by_id_crud(db=db, machine_id=machine_id)

    if not machine and raise_err:
        raise MachineNotFoundError(f"Machine with ID {machine_id} not found.")

    return machine
