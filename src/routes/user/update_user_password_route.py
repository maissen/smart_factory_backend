from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.schema.user_schema import UserUpdatePasswordRequest
from src.core.settings import settings

from src.services.user.update_user_password_service import update_password_service
from src.exceptions.user_exceptions import (
    InvalidPasswordError,
    InvalidUserIdError,
    MissingPasswordError,
    IncorrectPasswordError,
    PasswordUpdateError,
    UserNotAllowedError
)



router = APIRouter(prefix="", tags=["Users"])


@router.put("/update/password/{user_id}")
def update_password(
    user_id: int,
    payload: UserUpdatePasswordRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):

    try:
        # Ensure users can only change their own password unless admin privilege exists
        if current_user.id != user_id and current_user.role != settings.USER_ALLOWED_ROLES[0]:
            raise UserNotAllowedError("You do not have permission to change another user's password.")
        
        update_password_service(
            db=db,
            user_id=user_id,
            old_password=payload.old_password,
            new_password=payload.new_password
        )

        return {"message": "Password updated successfully"}

    except InvalidUserIdError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except MissingPasswordError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
    except InvalidPasswordError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except IncorrectPasswordError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

    except PasswordUpdateError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
    except UserNotAllowedError as e:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(e))

    except Exception:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Unexpected server error")
