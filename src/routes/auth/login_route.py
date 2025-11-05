from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.dependencies.postgres_dependency import get_db
from src.schema.token_schema import TokenLoginRequest, TokenResponse
from src.exceptions.user_exceptions import EmailDoesNotExistError, UserAuthenticationError, IncorrectPasswordError
from src.services.auth.login_user_service import login_user_service

router = APIRouter(
    prefix="",
)

@router.post("", response_model=TokenResponse, status_code=status.HTTP_200_OK)
def login_user(user: TokenLoginRequest, db: Session = Depends(get_db)):
    """
    Authenticate a user and return a JWT access token.
    """
    try:
        token_response = login_user_service(
            db=db,
            email=user.email,
            password=user.password
        )
        return token_response

    except UserAuthenticationError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except IncorrectPasswordError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))
    
    except EmailDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    
    except Exception as e:
        # Catch-all for unexpected errors
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error happened.")
