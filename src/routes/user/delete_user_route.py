from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.services.user.delete_user_service import delete_user_by_id_service
from src.exceptions.user_exceptions import InvalidUserIdError, UserDeletionError, UserNotAllowedError
from src.core.settings import settings

router = APIRouter(
    prefix="",
    tags=["users"]
)

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
    
    # Authorization check
    if current_user.role != settings.USER_ALLOWED_ROLES[0]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to perform this action."
        )

    # Attempt deletion and handle service-level exceptions
    try:
        delete_user_by_id_service(db=db, user_id=user_id)

    except UserNotAllowedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    except InvalidUserIdError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except UserDeletionError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

    # No return needed for 204 status
