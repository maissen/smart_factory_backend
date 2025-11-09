from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.schema.machine_schema import (
    MachineCreateRequestSchema,
    MachineResponseSchema
)
from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.services.machine.create_machine_service import create_machine_service
from src.models.user_model import User

router = APIRouter()


@router.post("/create", response_model=MachineResponseSchema, status_code=status.HTTP_201_CREATED)
def create_machine(
    request: MachineCreateRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    machine = create_machine_service(
        db=db,
        name=request.name,
        serial_number=request.serial_number,
        status=request.status,
        description=request.description,
        user_id=current_user.id
    )
    return machine