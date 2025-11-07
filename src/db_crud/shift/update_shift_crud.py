from src.db_crud.shift.get_shift_crud import get_shift_by_id_crud
from sqlalchemy.orm import Session

from src.models.shifts_model import Shift


def update_shift_crud(db: Session, shift_id: int, **kwargs) -> Shift:
    """
    Update shift attributes. Only updates provided fields.
    """
    shift = get_shift_by_id_crud(db, shift_id)

    for field, value in kwargs.items():
        if value is not None:
            setattr(shift, field, value)

    db.commit()
    db.refresh(shift)
    return shift