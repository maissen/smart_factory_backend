from pydantic import BaseModel, EmailStr
from datetime import datetime


# Request Schemas
class TokenLoginRequest(BaseModel):
    """
    Payload for login request.
    what the user sends to /login (email + password).
    """
    email: str
    password: str


# Response Schemas
class TokenResponse(BaseModel):
    """
    Response containing the JWT access token.
    what the API returns on successful login (access_token + type).
    """
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    """
    Payload data stored inside the JWT token.
    """
    user_id: int
    role: str
    expiration_time: int  # Expiration timestamp
