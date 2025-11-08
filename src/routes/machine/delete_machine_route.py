from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from src.dependencies.get_current_user_dependency import get_current_user
from src.dependencies.postgres_dependency import get_db
from src.services.machine.delete_machine_service import delete_machine_service


router = APIRouter()


@router.delete("/delete/{machine_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_machine(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    delete_machine_service(db=db, machine_id=machine_id, user_id=current_user.id)
