from influxdb_client.client.write_api import SYNCHRONOUS
from src.helpers.format_metric_service import format_metrics_for_influx
from src.core.settings import settings

def insert_metrics_service(data, influx_client):
    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    # Always format metrics as points (remove the influx_line check)
    points = format_metrics_for_influx(data.metrics)
    write_api.write(
        bucket=settings.INFLUXDB_BUCKET,
        org=settings.INFLUXDB_ORG,
        record=points
    )
    
    return {"message": f"Inserted {len(data.metrics)} metrics", "format": "point_objects"}