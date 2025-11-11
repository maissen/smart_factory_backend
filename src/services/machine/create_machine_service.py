from sqlalchemy.orm import Session

from src.db_crud.machine.machine_crud import create_machine_crud
from src.exceptions.machine_exceptions import *
from src.helpers.str_helpers import is_valid_str, normalize_str
from src.services.machine.get_machine_service import get_machine_by_serial_service, get_machine_by_name_service
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.core.settings import settings


def create_machine_service(
    db: Session,
    name: str,
    serial_number: str,
    user_id: int,
    status: str = settings.MACHINE_POSSIBLE_STATUS[1], # Idle
    description: str = None,
    last_maintenance_date=None,
):
    """Service to create a new machine."""

    # Check factory existance
    factory = get_factory_of_user_service(db=db, user_id=user_id)

    is_valid_str(name)
    name = normalize_str(name)

    machine_by_name = get_machine_by_name_service(db=db, name=name, raise_err=False)
    if machine_by_name:
        raise MachineNameAlreadyExistsError()

    is_valid_str(serial_number)
    serial_number = normalize_str(serial_number)

    machine_by_serial_nb = get_machine_by_serial_service(db=db, serial_number=serial_number, raise_err=False)
    if machine_by_serial_nb:
        raise MachineSerialNumberAlreadyExistsError()

    try:
        new_machine = create_machine_crud(
            db=db,
            factory_id=factory.id,
            name=name,
            serial_number=serial_number,
            last_maintenance_date=last_maintenance_date,
            description=description,
        )
        
        return new_machine
        
    except Exception as e:
        print(e)
        raise MachineError("Failed to create new machine.")


