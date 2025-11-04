from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# -------------------------------
# Base schema (optional fields)
# -------------------------------
class UserBase(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    role: Optional[str] = None


# -------------------------------
# Request schemas
# -------------------------------
class UserCreate(UserBase):
    full_name: str
    email: str
    password: str
    role: str
    phone_number: str


class UserUpdate(UserBase):
    pass  # all fields optional


class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str


# -------------------------------
# Response schemas
# -------------------------------
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


class UserCreateResponse(UserResponse):
    pass


class PasswordUpdateResponse(BaseModel):
    message: str
