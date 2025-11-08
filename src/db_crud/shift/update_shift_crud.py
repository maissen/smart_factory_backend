from src.db_crud.shift.get_shift_crud import get_shift_by_id_crud
from sqlalchemy.orm import Session
from src.models.shifts_model import Shift


def update_shift_crud(
    db: Session,
    shift_id: int,
    name: str = None,
    start_time: str = None,
    end_time: str = None
) -> Shift:
    """
    Update shift attributes.
    """
    shift = get_shift_by_id_crud(db, shift_id)

    if name is not None:
        shift.name = name

    if start_time is not None:
        shift.start_time = start_time

    if end_time is not None:
        shift.end_time = end_time

    db.commit()
    db.refresh(shift)
    return shift
