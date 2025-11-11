from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class MachineCreateRequestSchema(BaseModel):
    name: str
    serial_number: str
    status: str
    description: str


class MachineUpdateRequestSchema(BaseModel):
    name: str
    serial_number: str
    description: str


class MachineResponseSchema(BaseModel):
    id: int
    name: str
    serial_number: str
    status: str
    description: str
    last_maintenance_date: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime


class MachineStatusUpdateRequestSchema(BaseModel):
    status: str

