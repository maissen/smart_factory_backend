from fastapi import APIRouter, Depends, HTTPException, status
from src.schema.machine_schema import MachineResponseSchema, MachineUpdateRequestSchema
from sqlalchemy.orm import Session
from src.dependencies.get_current_user_dependency import get_current_user
from src.dependencies.postgres_dependency import get_db
from src.services.machine.delete_machine_service import delete_machine_service
from src.exceptions.machine_exceptions import *


router = APIRouter()


@router.delete("/delete/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        delete_machine_service(db=db, machine_id=machine_id, user_id=current_user.id)
    except (MachineNotFoundError, MachineAccessDeniedError, MachineError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
