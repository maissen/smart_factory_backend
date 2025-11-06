from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user

from src.services.user.get_user_by_email_optional_service import get_user_by_email_optional_service
from src.services.user.get_user_by_phone_number_optional_service import get_user_by_phone_number_optional_service

from src.schema.user_schema import UserUpdateRequest, UserResponse
from src.services.user.update_user_service import update_user_service
from src.core.settings import settings

from src.exceptions.user_exceptions import (
    InvalidUserIdError,
    InvalidFullNameError,
    EmailAlreadyExistsError,
    PhoneNumberAlreadyExistsError,
    UserUpdateError,
    UserNotAllowedError
)

router = APIRouter(prefix="", tags=["Users"])


@router.put("/update/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # Prevent updating another user's profile (unless for admin users)
    if current_user.role != settings.USER_ALLOWED_ROLES[0] and current_user.id != user_id:
        raise UserNotAllowedError("You are not allowed to update someone else's credentials.")

    # Perform update
    updated_user = update_user_service(
        db=db,
        user_id=user_id,
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
    )
    return updated_user

    try:
        pass

    except UserNotAllowedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    except InvalidUserIdError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except InvalidFullNameError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except PhoneNumberAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except UserUpdateError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")
