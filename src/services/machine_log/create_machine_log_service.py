from sqlalchemy.orm import Session

from src.exceptions.machine_log_exceptions import *
from src.core.settings import settings
from src.services.machine.get_machine_service import get_machine_by_id_service
from src.helpers.machine import validate_machine_id
from src.db_crud.machine_log.create_machine_log import create_machine_log_crud
from src.helpers.str_helpers import is_valid_str


def create_machine_log_service(
    db: Session,
    machine_id: int,
    machine_status: str,
    log_note: str
):
    
    # validate machine id
    validate_machine_id(machine_id)

    # validate str inputs
    is_valid_str(value=machine_status, raise_on_error=True, err_msg="Log status must be non-valid status string.")
    is_valid_str(value=log_note, raise_on_error=True, err_msg="Log note must be non-valid string.")

    # Check machine exists
    machine = get_machine_by_id_service(db=db, machine_id=machine_id)

    # validate status
    valid_statuses = settings.MACHINE_POSSIBLE_STATUS

    if machine_status and machine_status not in valid_statuses:
        raise InvalidMachineLogStatusError(f"Status must be one of {valid_statuses}")

    log = create_machine_log_crud(db=db, machine_id=machine_id, status=machine_status, notes=log_note)
    return log