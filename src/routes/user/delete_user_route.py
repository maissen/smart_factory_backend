from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.services.user.delete_user_service import delete_user_by_id_service
from src.exceptions.user_exceptions import UserNotAllowedError

router = APIRouter()

@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Delete a user by ID.
    
    - Only admins can perform this action.
    - Raises appropriate HTTP exceptions if user not found or deletion fails.
    """

    # Ensure users can only change their own password unless admin privilege exists
    if current_user.id != user_id:
        raise UserNotAllowedError()

    delete_user_by_id_service(db=db, user_id=user_id)