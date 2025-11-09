from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.schema.user_schema import UserUpdatePasswordRequest
from src.core.settings import settings

from src.services.user.update_user_password_service import update_password_service
from src.exceptions.user_exceptions import (
    UserNotAllowedError
)



router = APIRouter()


@router.put("/{user_id}/password", status_code=status.HTTP_204_NO_CONTENT)
def update_password(
    user_id: int,
    payload: UserUpdatePasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    # Ensure users can only change their own password unless admin privilege exists
    if current_user.id != user_id:
        raise UserNotAllowedError()
    
    
    update_password_service(
        db=db,
        user_id=user_id,
        old_password=payload.old_password,
        new_password=payload.new_password
    )
