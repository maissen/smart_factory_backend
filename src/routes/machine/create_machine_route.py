from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from src.schema.machine_schema import (
    MachineCreateRequestSchema,
    MachineUpdateRequestSchema,
    MachineResponseSchema
)
from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.services.machine.create_machine_service import create_machine_service
from src.exceptions.machine_exceptions import (
    MachineError,
    MachineNotFoundError,
    MachineNameAlreadyExistsError,
    MachineSerialNumberAlreadyExistsError,
    InvalidMachineStatusError,
    MachineAccessDeniedError
)
from src.models.user_model import User

router = APIRouter()


@router.post("/create/{factory_id}", response_model=MachineResponseSchema, status_code=status.HTTP_201_CREATED)
def create_machine(
    factory_id: int,
    request: MachineCreateRequestSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    try:
        machine = create_machine_service(
            db=db,
            factory_id=factory_id,
            name=request.name,
            serial_number=request.serial_number,
            status=request.status,
            description=request.description
        )
        return machine

    except (MachineNameAlreadyExistsError, MachineSerialNumberAlreadyExistsError, InvalidMachineStatusError, MachineError) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
