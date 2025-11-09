from typing import List
from src.schema.influx_db import MachineMetric

def format_metrics_for_influx(metrics: List[MachineMetric]) -> List[str]:
    """
    Converts MachineMetric items into InfluxDB line protocol strings.
    """
    lines = []
    for m in metrics:
        line = (
            f"machine_metrics,"
            f"machine_id={m.machine_id},machine_name={m.machine_name.replace(' ', '_')},status={m.status} "
            f"temperature={m.temperature},power_usage={m.power_usage} "
            f"{int(m.timestamp.timestamp() * 1_000_000_000)}"
        )
        lines.append(line)
    return lines
