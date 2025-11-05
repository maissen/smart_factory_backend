from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.dependencies.postgres_dependency import get_db
from src.schema.user_schema import UserCreate, UserCreateResponse
# Change this import:
from db_crud.users.create_user_crud import create_user_crud

router = APIRouter(
    prefix="/register",
)

@router.post("/", response_model=UserCreateResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user (client or admin depending on role).
    """
    try:
        new_user = create_user(
            db=db,
            full_name=user.full_name,
            email=user.email,
            password=user.password,
            role=user.role,
            phone_number=user.phone_number
        )
        return new_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )