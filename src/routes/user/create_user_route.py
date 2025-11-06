from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.dependencies.postgres_dependency import get_db
from src.schema.user_schema import UserRegisterRequest, UserResponse
from src.services.user.create_user_service import create_user_service
from src.exceptions.user_exceptions import (
    InvalidFullNameError,
    InvalidEmailError,
    InvalidPasswordError,
    InvalidPhoneNumberError,
    EmailAlreadyExistsError,
    PhoneNumberAlreadyExistsError,
    UserCreationError,
    InvalidRoleError,
    EmptyRoleError
)

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

    try:
        new_user = create_user_service(
            db=db,
            full_name=user.full_name,
            email=user.email,
            password=user.password,
            role=user.role,
            phone_number=user.phone_number
        )
        return new_user

    except InvalidFullNameError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except InvalidEmailError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except InvalidPasswordError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except InvalidPhoneNumberError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except EmptyRoleError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except InvalidRoleError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except EmailAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except PhoneNumberAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    
    except UserCreationError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    except Exception as e:
        # Fallback for unexpected errors
        print(e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Unexpected error happend while creating user.")