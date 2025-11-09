from fastapi import APIRouter, Depends
from src.schema.machine_schema import MachineResponseSchema
from src.schema.influx_db import MetricsResponse
from src.dependencies.influx_dependency import get_influx_client
from src.helpers.format_metric_service import format_metrics_for_influx
from src.core.settings import settings

router = APIRouter()


@router.post("/insert", response_model=MachineResponseSchema)
def insert_metrics(data: MetricsResponse, influx=Depends(get_influx_client)):
    write_api = influx.write_api(write_options=None)

    lines = format_metrics_for_influx(data.metrics)

    write_api.write(
        bucket=settings.INFLUXDB_BUCKET,
        org=settings.INFLUXDB_ORG,
        record=lines
    )

    return {"status": "success", "inserted": data.metrics_count}
