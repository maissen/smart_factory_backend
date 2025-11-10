
"""
Helper service to format metrics data for InfluxDB line protocol
"""
from typing import List
from datetime import datetime

def format_metrics_for_influx(metrics: List) -> List[str]:
    """
    Convert metrics to InfluxDB line protocol format
    
    Line protocol format:
    measurement,tag1=value1,tag2=value2 field1=value1,field2=value2 timestamp
    
    Example:
    machine_metrics,machine_id=18,machine_name=CNC_Mill,status=Running temperature=67.56,power_usage=365.98 1699603200000000000
    """
    lines = []
    
    for metric in metrics:
        # Parse timestamp to nanoseconds (InfluxDB uses nanosecond precision)
        if isinstance(metric.timestamp, str):
            dt = datetime.fromisoformat(metric.timestamp.replace('Z', '+00:00'))
        else:
            dt = metric.timestamp
        
        # Convert to nanoseconds since epoch
        timestamp_ns = int(dt.timestamp() * 1_000_000_000)
        
        # Escape special characters in tag values (spaces, commas, equals)
        machine_name_escaped = str(metric.machine_name).replace(' ', '_').replace(',', '\\,').replace('=', '\\=')
        status_escaped = str(metric.status).replace(' ', '_').replace(',', '\\,').replace('=', '\\=')
        
        # Build line protocol string
        # Format: measurement,tags fields timestamp
        line = (
            f"machine_metrics,"
            f"machine_id={metric.machine_id},"
            f"machine_name={machine_name_escaped},"
            f"status={status_escaped} "
            f"temperature={metric.temperature},"
            f"power_usage={metric.power_usage} "
            f"{timestamp_ns}"
        )
        
        lines.append(line)
    
    return lines