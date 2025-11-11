from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.schema.machine_log_schema import *
from src.services.machine_log.create_machine_log_service import create_machine_log_service

router = APIRouter()

@router.post("/create", response_model=MachineLogResponseSchema, status_code=status.HTTP_201_CREATED)
def create_machine_log(
    payload: MachineLogCreateRequestSchema,
    db: Session = Depends(get_db),
):
    
    return create_machine_log_service(db=db, machine_id=payload.machine_id, machine_status=payload.status, log_note=payload.notes)