from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.services.shifts.get_shift_service import get_shift_of_factory_service

from src.schema.shift_schema import ShiftResponseSchema

router = APIRouter()


@router.get("/factory/{factory_id}", response_model=ShiftResponseSchema)
def get_shift_of_factory_route(
    factory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Get the shift associated with a specific factory.
    """
    return get_shift_of_factory_service(
        db=db, 
        factory_id=factory_id, 
    )