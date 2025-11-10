from fastapi import APIRouter, Depends, status
from influxdb_client.client.write_api import SYNCHRONOUS
from src.schema.influx_db import MetricsResponse
from src.dependencies.influx_dependency import get_influx_client
from src.helpers.format_metric_service import format_metrics_for_influx
from src.core.settings import settings

router = APIRouter()

@router.post("/insert", status_code=status.HTTP_201_CREATED)
def insert_metrics(data: MetricsResponse, influx=Depends(get_influx_client)):
    write_api = influx.write_api(write_options=SYNCHRONOUS)

    lines = format_metrics_for_influx(data.metrics)

    write_api.write(
        bucket=settings.INFLUXDB_BUCKET,
        org=settings.INFLUXDB_ORG,
        record=lines
    )

    return {"inserted": data.metrics_count}
