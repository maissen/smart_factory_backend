from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.dependencies.get_current_user_dependency import get_current_user
from src.models.user_model import User
from src.helpers.factory import validate_factory_id
from src.services.factory.get_factory_service import get_factory_by_id_service
from src.exceptions.user_exceptions import UserAuthorizationError
from src.services.machine_log.delete_logs_of_factory_service import delete_factory_machine_logs_service

router = APIRouter()

@router.delete("/factory/{factory_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_factory_machine_logs(
    factory_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    
    validate_factory_id(factory_id)

    factory = get_factory_by_id_service(db=db, factory_id=factory_id)
    if factory.owner_id != current_user.id:
        raise UserAuthorizationError("You're not authorized to delete this factory's logs.")

    delete_factory_machine_logs_service(db=db, factory_id=factory_id)
