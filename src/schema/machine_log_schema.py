from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class MachineLogCreateRequestSchema(BaseModel):
    machine_id: int
    status: Optional[str] = None
    notes: Optional[str] = None


class MachineLogResponseSchema(BaseModel):
    id: int
    machine_id: int
    status: Optional[str] = None
    notes: Optional[str] = None
    timestamp: datetime
