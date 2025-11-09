from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.services.factory.get_factory_service import (
    get_factory_by_id_service,
    list_factories_service,
    get_factory_of_user_service,
)
from src.exceptions.factory_exceptions import (
    FactoryPermissionError
)
from src.schema.factories_schema import FactoryResponse
from src.dependencies.get_current_user_dependency import get_current_user
from src.dependencies.admin_dependency import require_admin
from src.core.settings import settings

router = APIRouter()


@router.get("/", response_model=FactoryResponse)
def get_factory_of_user_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    factories = get_factory_of_user_service(db, current_user.id)
    return factories


@router.get("/", response_model=list[FactoryResponse])
def list_factories_route(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
    admin = Depends(require_admin)
):
    return list_factories_service(db)
