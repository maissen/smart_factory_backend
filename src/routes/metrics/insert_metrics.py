from fastapi import APIRouter, Depends, status
from influxdb_client.client.write_api import SYNCHRONOUS
from src.schema.influx_db import MetricsResponse
from src.dependencies.influx_dependency import get_influx_client
from src.helpers.format_metric_service import format_metrics_for_influx
from src.core.settings import settings

router = APIRouter()

@router.post("/insert", status_code=status.HTTP_201_CREATED)
def insert_metrics(data: MetricsResponse, influx=Depends(get_influx_client)):
    """
    Insert machine metrics into InfluxDB
    Accepts both influx_lines (line protocol) and metrics (structured data)
    """
    write_api = influx.write_api(write_options=SYNCHRONOUS)

    # Print timestamps in human readable format
    for m in data.metrics:
        print(
            f"Machine {m.machine_name} at {m.timestamp.strftime('%Y-%m-%d %H:%M:%S')} "
            f"Status={m.status}, Temp={m.temperature}°C, Power={m.power_usage}W"
        )

    # Check if influx_lines are provided (pre-formatted line protocol)
    if hasattr(data, 'influx_lines') and data.influx_lines:
        print(f"[InfluxDB] Using pre-formatted line protocol ({len(data.influx_lines)} lines)")
        
        # Write line protocol strings directly
        write_api.write(
            bucket=settings.INFLUXDB_BUCKET,
            org=settings.INFLUXDB_ORG,
            record=data.influx_lines  # Write line protocol strings directly
        )
    else:
        print(f"[InfluxDB] Converting metrics to Point objects ({len(data.metrics)} metrics)")
        
        # Fallback: Use Point-based formatting (more reliable for structured data)
        points = format_metrics_for_influx(data.metrics)
        
        write_api.write(
            bucket=settings.INFLUXDB_BUCKET,
            org=settings.INFLUXDB_ORG,
            record=points  # Write Point objects
        )

    return {
        "inserted": data.metrics_count,
        "bucket": settings.INFLUXDB_BUCKET,
        "org": settings.INFLUXDB_ORG,
        "format": "line_protocol" if hasattr(data, 'influx_lines') and data.influx_lines else "point_objects"
    }