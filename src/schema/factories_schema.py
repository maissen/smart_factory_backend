from pydantic import BaseModel
from datetime import datetime


class FactoryRegisterRequest(BaseModel):
    name: str
    location: str
    description: str


class FactoryUpdateRequest(BaseModel):
    name: str
    location: str
    description: str
    updated_at: str


class FactoryResponse(BaseModel):
    id: int
    name: str
    location: str
    description: str
    created_at: datetime
    updated_at: datetime