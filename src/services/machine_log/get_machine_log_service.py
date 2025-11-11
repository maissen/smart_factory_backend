from sqlalchemy.orm import Session
from src.helpers.machine import validate_machine_id
from src.db_crud.machine_log.get_machine_log import *
from src.exceptions.machine_log_exceptions import *
from src.helpers.validate_user_id import validate_user_id
from src.core.settings import settings
from src.services.machine.get_machine_service import get_machine_by_id_service
from src.db_crud.machine_log.get_machine_log import get_machine_logs_by_machine_id_crud
from src.services.factory.get_factory_service import get_factory_of_user_service





def get_machine_logs_service(db: Session, machine_id: int, current_user):
    """
    Service to retrieve all logs for a machine.
    Raises MachineLogNotFoundError if machine does not exist.
    Raises MachineLogAccessDeniedError if user is not allowed to access.
    """
    validate_machine_id(machine_id)
    validate_user_id(current_user.id)

    # Ensure machine existance
    machine = get_machine_by_id_service(db=db, machine_id=machine_id)
    
    factory = get_factory_of_user_service(db=db, user_id=current_user.id)

    # Optional: enforce ownership/client rules
    if factory.owner_id != current_user.id:
        raise MachineLogAccessDeniedError("You do not have access to this machine's logs.")

    # Fetch logs
    try:
        machine_logs = get_machine_logs_by_machine_id_crud(db=db, machine_id=machine_id)
    except Exception as e:
        raise MachineLogFetchError()
    
    return machine_logs