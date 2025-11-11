from sqlalchemy.orm import Session

from src.models.machine_logs_model import MachineLog
from src.models.machine_model import Machine


def get_machine_logs_by_machine_id_crud(
    db: Session,
    machine_id: int,
) -> list[MachineLog]:
    """
    Retrieve all logs for a specific machine.
    """
    return db.query(MachineLog).filter(MachineLog.machine_id == machine_id).all()


def get_single_machine_log_by_id_crud(
    db: Session,
    log_id: int,
) -> MachineLog | None:
    """
    Retrieve a single machine log by its ID.
    Returns None if not found.
    """
    return db.query(MachineLog).filter(MachineLog.id == log_id).first()


def get_factory_machine_logs_crud(
    db: Session,
    factory_id: int,
) -> list[MachineLog]:
    """
    Retrieve all machine logs for all machines of a given factory.
    """
    return (
        db.query(MachineLog)
        .join(Machine)
        .filter(Machine.factory_id == factory_id)
        .all()
    )
