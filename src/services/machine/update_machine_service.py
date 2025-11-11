from datetime import date
from sqlalchemy.orm import Session
from src.db_crud.machine.machine_crud import update_machine_crud, update_machine_status_crud
from src.exceptions.machine_exceptions import *
from src.helpers.str_helpers import is_valid_str, normalize_str
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.services.machine.get_machine_service import get_machine_by_serial_service, get_machine_by_name_service, get_machine_by_id_service
from src.helpers.str_helpers import is_valid_str
from src.helpers.validate_user_id import validate_user_id
from src.core.settings import settings


def update_machine_service(
    db: Session,
    machine_id: int,
    user_id: int,
    name: str,
    serial_number: str,
    last_maintenance_date=None,
    description: str = None
):
    """Service to update an existing machine by ID with all fields."""

    validate_user_id(user_id)
    
    # check if factory exists
    factory = get_factory_of_user_service(db=db, user_id=user_id)

    # check if machine exists
    machine = get_machine_by_id_service(db=db, machine_id=machine_id)

    is_valid_str(name, raise_on_error=True, err_msg="Machine name must be a non-empty valid name.")
    name = normalize_str(name)

    machine_by_name = get_machine_by_name_service(db=db, name=name, raise_err=False)
    if machine_by_name:
        raise MachineNameAlreadyExistsError()

    is_valid_str(serial_number, raise_on_error=True, err_msg="Machine serial number must be a non-empty valid string.")
    serial_number = normalize_str(serial_number)
    machine_by_serial_nb = get_machine_by_serial_service(db=db, serial_number=serial_number, raise_err=False)
    
    if machine_by_serial_nb:
        raise MachineSerialNumberAlreadyExistsError()

    try:
        updated_machine = update_machine_crud(
            db=db,
            machine_id=machine_id,
            name=name,
            serial_number=serial_number,
            last_maintenance_date=last_maintenance_date,
            description=description
        )

    except Exception as e:  
        print(e)
        raise MachineError("Failed to update machine.")

    return updated_machine



def update_machine_status_service(
    db: Session,
    machine_id: int,
    status: str,
):
    """
    Update only the status of a machine.
    """

    # Ensure machine exists
    machine = get_machine_by_id_service(db=db, machine_id=machine_id)

    # Validate new status
    is_valid_str(status, raise_on_error=True, err_msg="Machine status must be a non-empty valid string.")
    status = normalize_str(status)

    if status not in settings.MACHINE_POSSIBLE_STATUS:
        raise InvalidMachineStatusError("Invalid machine status.")

    # Determine if maintenance date should be set (transitioning OUT of Maintenance)
    is_leaving_maintenance = (
        machine.status == settings.MACHINE_POSSIBLE_STATUS[2]  # "Maintenance"
        and status != settings.MACHINE_POSSIBLE_STATUS[2]
    )

    maintenance_date = date.today() if is_leaving_maintenance else None

    try:
        updated_machine = update_machine_status_crud(
            db=db,
            machine_id=machine_id,
            status=status,
            maintenance_date=maintenance_date
        )
    except Exception:
        raise MachineError("Failed to update machine status.")

    return updated_machine