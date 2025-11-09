from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.schema.factories_schema import FactoryUpdateRequest, FactoryResponse
from src.services.factory.update_factory_service import update_factory_service
from src.dependencies.get_current_user_dependency import get_current_user

from src.exceptions.factory_exceptions import (
    FactoryNotFoundError,
    FactoryPermissionError,
    FactoryUpdateError,
    InvalidFactoryIdError,
)


router = APIRouter()


@router.put("/update", response_model=FactoryResponse)
def update_factory(
    payload: FactoryUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Perform the update
    factory = update_factory_service(
        db=db,
        user_id=current_user.id,
        name=payload.name,
        location=payload.location,
        description=payload.description,
    )
    return factory
