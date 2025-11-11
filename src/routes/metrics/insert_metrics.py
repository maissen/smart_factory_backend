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

router = APIRouter()

@router.post("/insert", status_code=status.HTTP_200_OK)
def insert_metrics(
    data: MetricsRequest, 
    influxdb=Depends(get_influx_client),
    db=Depends(get_db)
):

    all_users = get_all_users_service(db=db, role=settings.USER_ALLOWED_ROLES[1])

    for user in all_users:

        factory = get_factory_of_user_service(db=db, user_id=user.id, raise_error=False)
        if not factory:
            continue

        shift = get_shift_of_factory_service(db=db, factory_id=factory.id, raise_error=False)
        if not shift:
            continue

        machines = get_all_factory_machines_service(db=db, user_id=user.id, factory_id=factory.id)
        factory_machine_ids = {m.id for m in machines}

        # Filter metrics to match:
        #   1) Machine belongs to the factory
        #   2) Metric timestamp inside shift hours
        filtered_metrics = [
            metric for metric in data.metrics
            if metric.machine_id in factory_machine_ids
            and is_within_shift(metric.timestamp, shift.start_time, shift.end_time)
        ]

        # insert the metrics
        if filtered_metrics:
            filtered_request = MetricsRequest(
                timestamp=data.timestamp,
                metrics=filtered_metrics
            )

        insert_metrics_service(filtered_request, influxdb)