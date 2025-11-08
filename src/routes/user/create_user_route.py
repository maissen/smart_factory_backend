from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.dependencies.postgres_dependency import get_db
from src.schema.user_schema import UserRegisterRequest, UserResponse
from src.services.user.create_user_service import create_user_service

router = APIRouter()


@router.post(
    "/register", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED
)
def register_user(user: UserRegisterRequest, db: Session = Depends(get_db)):
    """
    Register a new user (client or admin depending on role).
    """

    new_user = create_user_service(
        db=db,
        full_name=user.full_name,
        email=user.email,
        password=user.password,
        role=user.role,
        phone_number=user.phone_number
    )
    return new_user