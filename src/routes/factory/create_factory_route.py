from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.schema.factories_schema import (
    FactoryRegisterRequest,
    FactoryResponse,
)
from src.services.factory.create_factory_service import create_factory_service
from src.dependencies.get_current_user_dependency import get_current_user

from src.exceptions.factory_exceptions import (
    FactoryOwnerNotFoundError,
    FactoryAlreadyExistsError,
)

from src.exceptions.user_exceptions import (
    InvalidUserIdError,
    UserNotFoundError,
    UserFetchError,
)


router = APIRouter()


@router.post("/create", response_model=FactoryResponse, status_code=status.HTTP_201_CREATED)
def create_factory_route(
    payload: FactoryRegisterRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Create a factory. 
    Client can only create factories for themselves.
    """
    try:        
        factory = create_factory_service(
            db=db,
            name=payload.name,
            location=payload.location,
            description=payload.description,
            owner_id=current_user.id,
        )
        return factory

    # ---- USER-SIDE EXCEPTIONS ----
    except InvalidUserIdError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except UserFetchError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    # ---- FACTORY-SIDE EXCEPTIONS ----
    except FactoryOwnerNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except FactoryAlreadyExistsError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected server error while creating factory."
        )
