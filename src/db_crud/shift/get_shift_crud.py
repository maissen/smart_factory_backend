from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from src.models.shifts_model import Shift



def get_shift_by_factory_id_crud(db: Session, factory_id: int) -> Shift | None:
    """
    Get the shift for a given factory. Returns None if no shift exists.
    """
    return db.query(Shift).filter(Shift.factory_id == factory_id).first()


def get_shift_by_id_crud(db: Session, shift_id: int) -> Shift:
    """
    Get shift by ID. Raises if not found, so service layer can handle.
    """
    shift = db.query(Shift).filter(Shift.id == shift_id).first()
    if shift is None:
        raise NoResultFound(f"Shift with id={shift_id} not found.")
    return shift

