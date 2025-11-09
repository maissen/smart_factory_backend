from sqlalchemy.orm import Session

from src.db_crud.machine.machine_crud import delete_machine_crud
from src.services.machine.get_machine_service import get_all_factory_machines_service
from src.exceptions.machine_exceptions import *
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.helpers.validate_user_id import validate_user_id
from src.helpers.machine import validate_machine_id



def delete_machine_service(db: Session, machine_id: int, user_id: int):
    """Service to delete a machine by ID."""

    validate_user_id(user_id)
    validate_machine_id(machine_id)

    factory = get_factory_of_user_service(db=db, user_id=user_id)
    
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

    deleted_machine = delete_machine_crud(db=db, machine_id=machine_id)