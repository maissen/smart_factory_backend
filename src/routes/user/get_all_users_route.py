from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from src.dependencies.postgres_dependency import get_db
from src.services.user.get_all_users_service import get_all_users_service
from src.schema.user_schema import UserResponse
from src.dependencies.get_current_user_dependency import get_current_user
from src.dependencies.admin_dependency import require_admin

router = APIRouter()

@router.get("/", response_model=list[UserResponse])
def get_all_users(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user),
    admin = Depends(require_admin),
    role=Query(default=None, description="Optional role to filter users by")
):
    """
    Get all users. Only admin users can access this route.
    Optional query parameter `role` to filter users by role.
    """

    users = get_all_users_service(db, role=role)
    return users
