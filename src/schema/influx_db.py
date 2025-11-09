from pydantic import BaseModel
from typing import List
from datetime import datetime

class MachineMetric(BaseModel):
    machine_id: int
    machine_name: str
    status: str
    timestamp: datetime
    temperature: float
    power_usage: float

class MetricsResponse(BaseModel):
    timestamp: datetime
    metrics_count: int
    metrics: List[MachineMetric]
