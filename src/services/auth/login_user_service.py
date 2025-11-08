from sqlalchemy.orm import Session
from src.core.settings import settings
from src.helpers.security import create_access_token
from src.services.user.get_user_by_email_service import get_user_by_email_service
from src.exceptions.user_exceptions import IncorrectPasswordError
from src.core.security_config import pwd_context
from src.schema.token_schema import TokenResponse, TokenPayload
from datetime import datetime, timezone, timedelta

def login_user_service(db: Session, email: str, password: str) -> TokenResponse:
    """
    Authenticates a user and returns access token as TokenResponse.

    Raises:
        UserAuthenticationError: If user with email does not exist.
        IncorrectPasswordError: If password does not match.
    """
    user = get_user_by_email_service(db, email)

    if not pwd_context.verify(password, user.password_hash):
        raise IncorrectPasswordError()

    # Prepare token payload
    expiration_time = datetime.now(tz=timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    payload_data = TokenPayload(
        user_id=user.id,
        role=user.role,
        expiration_time=int(expiration_time.timestamp())
    )

    # Create JWT token
    access_token = create_access_token(data=payload_data.dict())

    # Return Pydantic response
    return TokenResponse(access_token=access_token, token_type="bearer")
