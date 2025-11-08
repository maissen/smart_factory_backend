from datetime import datetime, time
from pydantic import BaseModel


class ShiftCreateSchema(BaseModel):
    name: str
    start_time: time
    end_time: time


class ShiftUpdateSchema(BaseModel):
    name: str
    start_time: time
    end_time: time


class ShiftResponseSchema(BaseModel):
    id: int
    factory_id: int
    name: str
    start_time: time
    end_time: time
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
