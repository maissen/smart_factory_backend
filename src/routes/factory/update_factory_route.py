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


@router.put("/update/{factory_id}", response_model=FactoryResponse)
def update_factory(
    factory_id: int,
    update_data: FactoryUpdateRequest,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    # Perform the update
    factory = update_factory_service(
        db=db,
        factory_id=factory_id,
        user_id=current_user.id,
        name=update_data.name,
        location=update_data.location,
        description=update_data.description,
    )
    return factory
