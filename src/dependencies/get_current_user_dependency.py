from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timezone

from src.dependencies.postgres_dependency import get_db
from src.schema.token_schema import TokenPayload
from src.services.user.get_user_by_email_optional_service import get_user_by_email_optional_service
from src.core.settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")  # login route

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """
    Dependency to retrieve the currently authenticated user from JWT token.

    Raises:
        HTTPException: If token is invalid, expired, or user not found.
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(
            user_id=payload.get("user_id"),
            role=payload.get("role"),
            expiration_time=payload.get("expiration_time"),
        )

        # Check expiration
        if datetime.now(tz=timezone.utc).timestamp() > token_data.expiration_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired")

    except JWTError:
        raise credentials_exception

    # Fetch user from DB
    user = get_user_by_email_optional_service(db, token_data.user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist.")

    return user
