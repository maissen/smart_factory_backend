from fastapi import APIRouter, Depends, status
from src.dependencies.influx_dependency import get_influx_client
from src.dependencies.postgres_dependency import get_db
from src.schema.influx_metric_schema import MetricsRequest
from src.services.metrics.insert_metrics_service import insert_metrics_service
from src.services.user.get_all_users_service import get_all_users_service
from src.services.factory.get_factory_service import get_factory_of_user_service
from src.services.shifts.get_shift_service import get_shift_of_factory_service
from src.services.machine.get_machine_service import get_all_factory_machines_service
from src.helpers.shifts import is_within_shift
from src.core.settings import settings
from src.services.metrics.filter_metrics_service import filter_metrics_service

router = APIRouter()

@router.post("/insert", status_code=status.HTTP_200_OK)
def insert_metrics(
    metrics: MetricsRequest, 
    influx_client=Depends(get_influx_client),
    db=Depends(get_db)
):
    
    filter_metrics_service(db=db, metrics=metrics, influx_client=influx_client)