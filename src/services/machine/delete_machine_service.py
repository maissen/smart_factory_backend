from sqlalchemy.orm import Session

from src.db_crud.machine.machine_crud import delete_machine_crud
from src.services.machine.get_machine_service import get_all_factory_machines_service
from src.exceptions.user_exceptions import UserAuthorizationError
from src.exceptions.machine_exceptions import (
    MachineNotFoundError,
    MachineAccessDeniedError
)
from src.services.factory.get_factory_service import get_factory_of_user_service



def delete_machine_service(db: Session, machine_id: int, user_id: int):
    """Service to delete a machine by ID."""

    factory = get_factory_of_user_service(db=db, user_id=user_id)
    if factory.owner_id != user_id:
        raise UserAuthorizationError("You're not authorized to perform this action.")
    
    machines = get_all_factory_machines_service(db=db, factory_id=factory.id, user_id=user_id)
    machine = None
    for m in machines:
        if m.id == machine_id:
            machine = m
            break
    else:
        raise MachineNotFoundError(f"Machine with ID {machine_id} not found.")
    
    if machine.factory_id != factory.id:
        raise MachineAccessDeniedError("You cannot update a machine from another factory.")

    deleted_machine = delete_machine_crud(db=db, machine_id=machine_id)
    return deleted_machine