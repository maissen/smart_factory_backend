from pydantic import BaseModel
from datetime import datetime

class MachineCreateRequestSchema(BaseModel):
    name: str
    serial_number: str
    status: str
    description: str


class MachineUpdateRequestSchema(BaseModel):
    name: str
    serial_number: str
    status: str
    description: str


class MachineResponseSchema(BaseModel):
    name: str
    serial_number: str
    status: str
    description: str
    last_maintenance_date: datetime
    created_at: datetime
    updated_at: datetime


