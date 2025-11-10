from fastapi import APIRouter, Depends, status
from src.dependencies.influx_dependency import get_influx_client
from src.schema.influx_metric_schema import MetricsRequest
from src.services.metrics.insert_metrics_service import insert_metrics_service

router = APIRouter()

@router.post("/insert", status_code=status.HTTP_200_OK)
def insert_metrics(data: MetricsRequest, influx=Depends(get_influx_client)):
    insert_metrics_service(data, influx)
    
