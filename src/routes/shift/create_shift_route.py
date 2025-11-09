from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user

from src.services.shifts.create_shift_service import create_shift_service

from src.schema.shift_schema import ShiftCreateSchema, ShiftResponseSchema


router = APIRouter()


@router.post("/create", response_model=ShiftResponseSchema, status_code=status.HTTP_201_CREATED)
def create_shift_route(
    data: ShiftCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a shift for a specific factory.
    """
    return create_shift_service(
        db=db,
        name=data.name,
        start_time=data.start_time,
        end_time=data.end_time,
        user_id=current_user.id,
    )

