from sqlalchemy.orm import Session
from src.exceptions.machine_log_exceptions import *
from src.db_crud.machine_log.delete_all_machine_logs import delete_factory_machine_logs_crud
from src.helpers.factory import validate_factory_id


def delete_factory_machine_logs_service(
    db: Session,
    factory_id: int,
):
    validate_factory_id(factory_id)

    if not delete_factory_machine_logs_crud(db=db, factory_id=factory_id):
        raise MachineLogDeleteError("An error occured while deleting logs for this factory.")
