from pydantic import BaseModel
from datetime import datetime
from src.core.settings import settings


class UserRegisterRequest(BaseModel):
    full_name: str
    email: str
    password: str
    role: str = settings.USER_ALLOWED_ROLES[1] # client
    phone_number: str



class UserUpdateRequest(BaseModel):
    full_name: str
    email: str
    phone_number: str



# Response schemas
class UserResponse(BaseModel):
    id: int
    full_name: str
    email: str
    role: str
    phone_number: str
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes": True
    }
