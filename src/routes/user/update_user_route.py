from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user

from src.schema.user_schema import UserUpdateRequest, UserResponse
from src.services.user.update_user_service import update_user_service
from src.core.settings import settings

from src.exceptions.user_exceptions import (
    UserNotAllowedError
)

router = APIRouter()


@router.put("/{user_id}/update", response_model=UserResponse)
def update_user(
    user_id: int,
    payload: UserUpdateRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
):
    # Prevent updating another user's profile (unless for admin users)
    if current_user.role != settings.USER_ALLOWED_ROLES[0] and current_user.id != user_id:
        raise UserNotAllowedError()

    # Perform update
    updated_user = update_user_service(
        db=db,
        user_id=user_id,
        full_name=payload.full_name,
        email=payload.email,
        phone_number=payload.phone_number,
    )
    return updated_user

    