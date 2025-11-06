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


class FactoryResponse(BaseModel):
    id: int
    owner_id: int
    name: str
    location: str
    description: str
    created_at: datetime
    updated_at: datetime