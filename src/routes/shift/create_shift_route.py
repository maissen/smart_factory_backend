from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user

from src.services.shifts.create_shift_service import create_shift_service

from src.schema.shift_schema import ShiftCreateSchema, ShiftResponseSchema
from src.exceptions.shifts_exceptions import (
    ShiftEndTimeIsInvalidError,
    ShiftNameIsInvalidError,
    ShiftNotFoundError,
    ShiftAlreadyExistsError,
    ShiftPermissionError,
    ShiftStartTimeIsInvalidError,
    ShiftTimeRangeError,
)


router = APIRouter()


@router.post("/create/{factory_id}", response_model=ShiftResponseSchema, status_code=status.HTTP_201_CREATED)
def create_shift_route(
    factory_id: int,
    data: ShiftCreateSchema,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Create a shift for a specific factory.
    """
    try:
        return create_shift_service(
            db=db,
            factory_id=factory_id,
            name=data.name,
            start_time=data.start_time,
            end_time=data.end_time,
            current_user=current_user,
        )

    except ShiftAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except ShiftNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except ShiftPermissionError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))
    
    except ShiftNameIsInvalidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except ShiftStartTimeIsInvalidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except ShiftEndTimeIsInvalidError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except ShiftTimeRangeError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="An error occurred while creating your shift")

