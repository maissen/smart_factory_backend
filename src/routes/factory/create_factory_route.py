from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.schema.factories_schema import (
    FactoryRegisterRequest,
    FactoryResponse,
)
from src.services.factory.create_factory_service import create_factory_service
from src.dependencies.get_current_user_dependency import get_current_user


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
    factory = create_factory_service(
        db=db,
        name=payload.name,
        location=payload.location,
        description=payload.description,
        owner_id=current_user.id,
    )
    return factory
