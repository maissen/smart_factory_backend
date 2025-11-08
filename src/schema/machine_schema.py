from pydantic import BaseModel
from datetime import date

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
    last_maintenance_date: date
    created_at: date
    updated_at: date


