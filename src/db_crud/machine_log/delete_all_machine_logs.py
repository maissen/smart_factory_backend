from sqlalchemy.orm import Session

from src.models.machine_logs_model import MachineLog
from src.models.machine_model import Machine



def delete_factory_machine_logs_crud(
    db: Session,
    factory_id: int,
) -> int:
    """
    Delete all machine logs for all machines of a specific factory.
    Returns the number of deleted logs.
    """
    logs_to_delete = (
        db.query(MachineLog)
        .join(Machine)
        .filter(Machine.factory_id == factory_id)
    )

    deleted_count = logs_to_delete.count()
    logs_to_delete.delete(synchronize_session=False)
    db.commit()
    return deleted_count