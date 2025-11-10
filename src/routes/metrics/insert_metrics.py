from fastapi import APIRouter, Depends, status
from src.schema.influx_db import MetricsResponse
from src.dependencies.influx_dependency import get_influx_client
from src.services.metrics.insert_metrics_service import insert_metrics_service

router = APIRouter()

@router.post("/insert", status_code=status.HTTP_204_NO_CONTENT)
def insert_metrics(data: MetricsResponse, influx=Depends(get_influx_client)):
    return insert_metrics_service(data, influx)
