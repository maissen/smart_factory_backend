from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.dependencies.postgres_dependency import get_db
from src.services.machine.get_machine_service import load_all_machines_service
from src.schema.machine_schema import MachineResponseSchema

router = APIRouter()


@router.get(
    "/all",
    response_model=list[MachineResponseSchema]
)
def load_all_machines(db: Session = Depends(get_db)):
    """
    Load all machines from all factories.
    No user or factory filtering.
    will be consumed by the iot metrics agent to fetch all machines and generate metrics for each
    """
    machines = load_all_machines_service(db=db)
    return machines
