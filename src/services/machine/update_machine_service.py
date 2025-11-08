from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db_crud.machine.machine_crud import update_machine_crud
from src.exceptions.machine_exceptions import (
    MachineError,
    MachineNotFoundError,
    MachineNameAlreadyExistsError,
    MachineSerialNumberAlreadyExistsError,
    InvalidMachineStatusError,
    MachineAccessDeniedError,
)
from src.exceptions.user_exceptions import UserAuthorizationError
from src.helpers.str_helpers import is_valid_str, normalize_str
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.services.machine.get_machine_service import get_all_factory_machines_service, get_machine_by_serial_service, get_machine_by_name_service
from src.core.settings import settings


def update_machine_service(
    db: Session,
    machine_id: int,
    user_id: int,
    name: str,
    serial_number: str,
    status: str,
    last_maintenance_date=None,
    description: str = None
):
    """Service to update an existing machine by ID with all fields."""
    
    factory = get_factory_of_user_service(db=db, user_id=user_id)
    if factory.owner_id != user_id:
        raise UserAuthorizationError()

    machines = get_all_factory_machines_service(db=db, factory_id=factory.id, user_id=user_id)
    machine = None
    for m in machines:
        if m.id == machine_id:
            machine = m
            break
    else:
        raise MachineNotFoundError()

    if machine.factory_id != factory.id:
        raise MachineAccessDeniedError()

    if not is_valid_str(name):
        raise MachineError()
    name = normalize_str(name)
    machine_by_name = get_machine_by_name_service(db=db, name=name, raise_if_not_found=False)
    if machine_by_name:
        raise MachineNameAlreadyExistsError()

    if not is_valid_str(serial_number):
        raise MachineError("Serial number is required.")
    serial_number = normalize_str(serial_number)
    machine_by_serial_nb = get_machine_by_serial_service(db=db, serial_number=serial_number, raise_if_not_found=False)
    if machine_by_serial_nb:
        print('machine is found')
        raise MachineSerialNumberAlreadyExistsError()

    if status not in settings.MACHINE_POSSIBLE_STATUS:
        raise InvalidMachineStatusError()

    try:
        updated_machine = update_machine_crud(
            db=db,
            machine_id=machine_id,
            name=name,
            serial_number=serial_number,
            status=status,
            last_maintenance_date=last_maintenance_date,
            description=description
        )

    except Exception as e:  
        raise MachineError()

    return updated_machine

