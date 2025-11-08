from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.services.machine.get_machine_service import get_all_factory_machines_service
from src.dependencies.get_current_user_dependency import get_current_user
from src.schema.machine_schema import MachineResponseSchema

router = APIRouter()


@router.get(
    "/factory/{factory_id}",
    response_model=list[MachineResponseSchema]
)
def list_factory_machines(factory_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    """
    Get all machines for a specific factory.
    Admins can fetch any factory's machines.
    Clients can fetch only their own factory's machines.
    """

    machines = get_all_factory_machines_service(
        db=db,
        user_id=current_user.id,
        factory_id=factory_id
    )
    return machines
