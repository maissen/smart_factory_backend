from fastapi import APIRouter, Depends, HTTPException, status
from src.schema.machine_schema import MachineResponseSchema, MachineUpdateRequestSchema
from sqlalchemy.orm import Session
from src.dependencies.get_current_user_dependency import get_current_user
from src.dependencies.postgres_dependency import get_db
from src.services.machine.update_machine_service import update_machine_service
from src.exceptions.machine_exceptions import *



router = APIRouter()


@router.put("/update/{machine_id}", response_model=MachineResponseSchema)
def update_machine(
    machine_id: int,
    request: MachineUpdateRequestSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    try:
        machine = update_machine_service(
            db=db,
            machine_id=machine_id,
            name=request.name,
            serial_number=request.serial_number,
            status=request.status,
            description=request.description,
            user_id=current_user.id
        )
        return machine

    except (
        MachineNotFoundError,
        MachineAccessDeniedError,
        MachineNameAlreadyExistsError,
        MachineSerialNumberAlreadyExistsError,
        InvalidMachineStatusError,
        MachineError
    ) as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))