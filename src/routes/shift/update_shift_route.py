from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import time

from src.dependencies.postgres_dependency import get_db
from src.services.shifts.update_shift_service import update_shift_service
from src.schema.shift_schema import ShiftUpdateSchema, ShiftResponseSchema
from src.dependencies.get_current_user_dependency import get_current_user

router = APIRouter()

@router.put("/update", response_model=ShiftResponseSchema)
def update_shift(
    payload: ShiftUpdateSchema,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """
    Update a shift by its ID.
    Only the factory owner (client) or admin can update a shift.
    """
    updated_shift = update_shift_service(
        db=db,
        name=payload.name,
        start_time=payload.start_time,
        end_time=payload.end_time,
        user_id=current_user.id
    )
    return updated_shift
