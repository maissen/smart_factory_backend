from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class MachineMetric(BaseModel):
    """Individual machine metric"""
    machine_id: int
    machine_name: str
    status: str
    timestamp: datetime
    timestamp_ns: int = Field(..., description="Timestamp in nanoseconds for InfluxDB")
    temperature: float = Field(..., description="Machine temperature in °C")
    power_usage: float = Field(..., description="Power consumption in watts")
    influx_line: Optional[str] = Field(None, description="Pre-formatted InfluxDB line protocol")

    class Config:
        json_schema_extra = {
            "example": {
                "machine_id": 1,
                "machine_name": "Machine_A",
                "status": "Running",
                "timestamp": "2025-11-10T10:30:00",
                "timestamp_ns": 1699876543000000000,
                "temperature": 75.5,
                "power_usage": 450.2,
                "influx_line": "machine_metrics,machine_id=1,machine_name=Machine_A,status=Running temperature=75.5,power_usage=450.2 1699876543000000000"
            }
        }


class MetricsResponse(BaseModel):
    """Response containing multiple machine metrics"""
    timestamp: datetime = Field(..., description="Batch timestamp")
    metrics_count: int = Field(..., description="Number of metrics in batch")
    metrics: List[MachineMetric] = Field(..., description="List of machine metrics")
    influx_lines: Optional[List[str]] = Field(
        None, 
        description="Pre-formatted InfluxDB line protocol strings (optional)"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "timestamp": "2025-11-10T10:30:00",
                "metrics_count": 2,
                "metrics": [
                    {
                        "machine_id": 1,
                        "machine_name": "Machine_A",
                        "status": "Running",
                        "timestamp": "2025-11-10T10:30:00",
                        "timestamp_ns": 1699876543000000000,
                        "temperature": 75.5,
                        "power_usage": 450.2,
                        "cycle_count": 1000,
                        "wear_level": 45.2
                    }
                ],
                "influx_lines": [
                    "machine_metrics,machine_id=1,machine_name=Machine_A,status=Running temperature=75.5,power_usage=450.2,cycle_count=1000i,wear_level=45.2 1699876543000000000"
                ]
            }
        }