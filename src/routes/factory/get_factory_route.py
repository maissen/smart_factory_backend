from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.services.factory.get_factory_service import (
    get_factory_by_id_service,
    list_factories_service,
    get_factory_of_user_service,
)
from src.exceptions.factory_exceptions import (
    InvalidFactoryIdError,
    FactoryPermissionError
)
from src.schema.factories_schema import FactoryResponse
from src.dependencies.get_current_user_dependency import get_current_user
from src.core.settings import settings

router = APIRouter()


@router.get("/{factory_id}", response_model=FactoryResponse)
def get_factory_by_id_route(
    factory_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Returns a single factory by ID.
    Accessible by admin or the factory owner.
    """
    # Validate user_id
    if not isinstance(factory_id, int):
        raise InvalidFactoryIdError()
    
    factory = get_factory_by_id_service(db, factory_id)

    # Permission check: only admin or the factory owner
    if current_user.role != settings.USER_ALLOWED_ROLES[0] and factory.owner_id != current_user.id:
        raise FactoryPermissionError("You're not authorized to fetch this factory's data.")

    return factory


@router.get("/user/{user_id}", response_model=FactoryResponse)
def get_factory_of_user_route(
    user_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Returns all factories owned by a specific user.
    Admins can view any user's factories.
    Clients can only view their own.
    """
    if current_user.role != settings.USER_ALLOWED_ROLES[0] and current_user.id != user_id:
        raise FactoryPermissionError()

    factories = get_factory_of_user_service(db, user_id)
    return factories


@router.get("/", response_model=list[FactoryResponse])
def list_factories_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    """
    Admin -> returns all factories
    Client -> returns only factories they own
    """
    admin_flag = current_user.role == settings.USER_ALLOWED_ROLES[0]
    if not admin_flag:
        raise FactoryPermissionError()

    return list_factories_service(db, admin=admin_flag, user_id=current_user.id)
