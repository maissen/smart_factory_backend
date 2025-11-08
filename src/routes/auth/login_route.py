from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.dependencies.postgres_dependency import get_db
from src.schema.token_schema import TokenLoginRequest, TokenResponse
from src.exceptions.user_exceptions import EmailDoesNotExistError, UserAuthenticationError, IncorrectPasswordError
from src.services.auth.login_user_service import login_user_service

router = APIRouter()

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(user: TokenLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.
    """
    token_response = login_user_service(
        db=db,
        email=user.email,
        password=user.password
    )
    return token_response
