from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from src.dependencies.postgres_dependency import get_db
from src.services.user.get_all_users_service import get_all_users_service
from src.schema.user_schema import UserResponse
from src.dependencies.get_current_user_dependency import get_current_user
from src.exceptions.user_exceptions import (
    UserFetchError,
    InvalidRoleError,
    EmptyRoleError
)
from src.core.settings import settings

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    role=Query(default=None, description="Optional role to filter users by")
):
    """
    Get all users. Only admin users can access this route.
    Optional query parameter `role` to filter users by role.
    """
    # Check admin role
    if current_user.role != settings.USER_ALLOWED_ROLES[0]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource."
        )

    try:
        users = get_all_users_service(db, role=role)
        return users

    except InvalidRoleError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except EmptyRoleError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

    except UserFetchError as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occured while fetching users."
        )
