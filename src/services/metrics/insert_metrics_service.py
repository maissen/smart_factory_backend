from influxdb_client.client.write_api import SYNCHRONOUS
from src.helpers.format_metric_service import format_metrics_for_influx
from src.core.settings import settings

def insert_metrics_service(data, influx_client):
    """
    Handles the insertion of metrics into InfluxDB.
    Accepts both pre-formatted line protocol (influx_lines) and structured metrics.
    """

    write_api = influx_client.write_api(write_options=SYNCHRONOUS)

    # Case 1: Client sends raw line protocol
    if hasattr(data, 'influx_lines') and data.influx_lines:

        write_api.write(
            bucket=settings.INFLUXDB_BUCKET,
            org=settings.INFLUXDB_ORG,
            record=data.influx_lines
        )

        result_format = "line_protocol"

    # Case 2: Structured metric list -> convert to Points
    else:
        points = format_metrics_for_influx(data.metrics)

        write_api.write(
            bucket=settings.INFLUXDB_BUCKET,
            org=settings.INFLUXDB_ORG,
            record=points
        )

        result_format = "point_objects"

    return {
        "inserted": data.metrics_count,
        "bucket": settings.INFLUXDB_BUCKET,
        "org": settings.INFLUXDB_ORG,
        "format": result_format
    }
