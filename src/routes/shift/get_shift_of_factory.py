from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.services.shifts.get_shift_service import get_shift_of_factory_service

from src.schema.shift_schema import ShiftResponseSchema
from src.exceptions.factory_exceptions import FactoryNotFoundError, InvalidFactoryIdError
from src.exceptions.shifts_exceptions import (
    ShiftNotFoundError,
    ShiftPermissionError,
)


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
    try:
        return get_shift_of_factory_service(
            db=db, 
            factory_id=factory_id, 
            current_user=current_user
        )

    except ShiftNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except ShiftPermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    except InvalidFactoryIdError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except FactoryNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
