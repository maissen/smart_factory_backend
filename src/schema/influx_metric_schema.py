from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class MachineMetric(BaseModel):
    machine_id: int
    machine_name: str
    status: str
    timestamp: datetime
    timestamp_ns: int
    temperature: float
    power_usage: float


class MetricsRequest(BaseModel):
    timestamp: datetime
    metrics: List[MachineMetric]

    @property
    def metrics_count(self) -> int:
        return len(self.metrics)