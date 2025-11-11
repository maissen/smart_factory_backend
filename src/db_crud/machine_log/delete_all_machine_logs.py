from sqlalchemy.orm import Session

from src.models.machine_logs_model import MachineLog
from src.models.machine_model import Machine



def delete_factory_machine_logs_crud(db: Session, factory_id: int) -> bool:
    """
    Delete all machine logs for all machines of a specific factory.
    """
    # Get all MachineLog IDs to delete
    log_ids = (
        db.query(MachineLog.id)
        .join(Machine)
        .filter(Machine.factory_id == factory_id)
        .all()
    )
    
    # Extract IDs from tuples
    log_ids = [id_tuple[0] for id_tuple in log_ids]

    if log_ids:
        db.query(MachineLog).filter(MachineLog.id.in_(log_ids)).delete(synchronize_session=False)
        db.commit()
    
    return True
