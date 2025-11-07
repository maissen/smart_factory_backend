from sqlalchemy.orm import Session

from src.models.shifts_model import Shift


def create_shift_crud(db: Session, factory_id: int, name: str, start_time, end_time) -> Shift:
    """
    Create a shift for a factory. Each factory can have only one shift.
    """
    shift = Shift(
        factory_id=factory_id,
        name=name,
        start_time=start_time,
        end_time=end_time,
    )
    db.add(shift)
    db.commit()
    db.refresh(shift)
    return shift