from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.models.user_model import User
from src.models.machine_logs_model import MachineLog
from src.models.machine_model import Machine
from src.schema.machine_log_schema import *
from src.exceptions.machine_log_exceptions import *
from src.services.machine_log.get_machine_log_service import get_machine_logs_service

router = APIRouter()


@router.get("/machine/{machine_id}", response_model=List[MachineLogResponseSchema])
def get_machine_logs(
    machine_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_machine_logs_service(db=db, machine_id=machine_id, current_user=current_user)


@router.get("/{log_id}", response_model=MachineLogResponseSchema)
def get_machine_log_by_id(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    log = db.query(MachineLog).filter(MachineLog.id == log_id).first()
    if not log:
        raise MachineLogNotFoundError()
    return log


@router.get("/factory/{factory_id}", response_model=List[MachineLogResponseSchema])
def get_factory_machine_logs(
    factory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    logs = db.query(MachineLog).join(Machine).filter(Machine.factory_id == factory_id).all()
    if not logs:
        raise MachineLogNotFoundError("No logs found for this factory")
    return logs