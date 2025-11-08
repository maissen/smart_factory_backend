from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.db_crud.machines import (
    create_machine_crud,
    update_machine_crud,
    delete_machine_crud,
    get_machine_by_id_crud,
    get_all_machines_crud
)
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
from src.core.settings import settings


def update_machine_service(
    db: Session,
    machine_id: int,
    factory_id: int,
    user_id: int,
    name: str,
    serial_number: str,
    status: str,
    last_maintenance_date=None,
    description: str = None
):
    """Service to update an existing machine by ID with all fields."""

    machine = get_machine_by_id_crud(db=db, machine_id=machine_id)
    if not machine:
        raise MachineNotFoundError(f"Machine with ID {machine_id} not found.")
    
    factory = get_factory_of_user_service(db=db, user_id=user_id)
    if not factory.owner_id != user_id:
        raise UserAuthorizationError("You're not authorized to perform this action.")

    if machine.factory_id != factory_id:
        raise MachineAccessDeniedError("You cannot update a machine from another factory.")

    if not is_valid_str(name):
        raise MachineError("Machine name is required.")
    name = normalize_str(name)

    if not is_valid_str(serial_number):
        raise MachineError("Serial number is required.")
    serial_number = normalize_str(serial_number)

    if status not in settings.MACHINE_POSSIBLE_STATUS:
        raise InvalidMachineStatusError(f"Invalid status: {status}")

    try:
        updated_machine = update_machine_crud(
            db=db,
            machine_id=machine_id,
            factory_id=factory_id,
            name=name,
            serial_number=serial_number,
            status=status,
            last_maintenance_date=last_maintenance_date,
            description=description
        )

    except IntegrityError as e:
        if "machines_name_key" in str(e.orig):
            raise MachineNameAlreadyExistsError(f"Machine name '{name}' already exists.")
        elif "machines_serial_number_key" in str(e.orig):
            raise MachineSerialNumberAlreadyExistsError(f"Serial number '{serial_number}' already exists.")
        else:
            print(e)
            raise MachineError(f"Unexpected database error.")

    return updated_machine

