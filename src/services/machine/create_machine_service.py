from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db_crud.machine.machine_crud import create_machine_crud
from src.exceptions.machine_exceptions import (
    MachineError,
    MachineNameAlreadyExistsError,
    MachineSerialNumberAlreadyExistsError,
    InvalidMachineStatusError,
    MachineInvalidNameError,
    MachineInvalidSerialNumberError
)
from src.helpers.str_helpers import is_valid_str, normalize_str

from src.core.settings import settings


def create_machine_service(
    db: Session,
    factory_id: int,
    name: str,
    serial_number: str,
    status: str = "Idle",
    last_maintenance_date=None,
    description: str = None
):
    """Service to create a new machine."""

    if not is_valid_str(name):
        raise MachineInvalidNameError("Machine name is required.")
    name = normalize_str(name)

    if not is_valid_str(serial_number):
        raise MachineInvalidSerialNumberError("Serial number is required.")
    serial_number = normalize_str(serial_number)

    if status not in settings.MACHINE_POSSIBLE_STATUS:
        raise InvalidMachineStatusError(f"Invalid status, possible statuses are : {settings.MACHINE_POSSIBLE_STATUS}")

    try:
        new_machine = create_machine_crud(
            db=db,
            factory_id=factory_id,
            name=name,
            serial_number=serial_number,
            status=status,
            last_maintenance_date=last_maintenance_date,
            description=description
        )
        
    except IntegrityError as e:
        if "machines_name_key" in str(e.orig):
            raise MachineNameAlreadyExistsError(f"Machine name already exists.")
        elif "machines_serial_number_key" in str(e.orig):
            raise MachineSerialNumberAlreadyExistsError(f"Serial number already exists.")
        else:
            print(e)
            raise MachineError(f"Unexpected database error")

    return new_machine

