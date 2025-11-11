from influxdb_client.client.write_api import SYNCHRONOUS
from src.schema.influx_metric_schema import MetricsRequest
from src.helpers.format_metric_service import format_metrics_for_influx
from src.core.settings import settings
from src.exceptions.tsdb_exceptions import TSDBConnectionError, TSDBWriteError

def insert_metrics_service(data: MetricsRequest, influx_client):
    try:
        write_api = influx_client.write_api(write_options=SYNCHRONOUS)
    except Exception:
        raise TSDBConnectionError()

    try:
        points = format_metrics_for_influx(data.metrics)
        write_api.write(
            bucket=settings.INFLUXDB_BUCKET,
            org=settings.INFLUXDB_ORG,
            record=points
        )
    except Exception:
        raise TSDBWriteError()

    return {"message": f"Inserted {len(data.metrics)} metrics", "format": "point_objects"}

