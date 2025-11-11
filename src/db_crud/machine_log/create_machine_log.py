from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.models.machine_logs_model import MachineLog
from src.models.machine_model import Machine


def create_machine_log_crud(
    db: Session,
    machine_id: int,
    status: str | None = None,
    notes: str | None = None,
) -> MachineLog:
    """
    Create a new machine log entry for a specific machine.
    """
    log = MachineLog(
        machine_id=machine_id,
        status=status,
        notes=notes,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log