from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError, InvalidSignatureError
from datetime import datetime, timezone

from src.dependencies.postgres_dependency import get_db
from src.schema.token_schema import TokenPayload
from src.core.settings import settings
from src.services.user.get_user_by_id_service import get_user_by_id_service

from src.exceptions.user_exceptions import (
    UserNotFoundError,
    InvalidEmailError
)

from src.exceptions.token_exceptions import (
    TokenExpiredError,
    InvalidTokenError
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_current_user(
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    """
    Validates JWT token, ensures it's not expired,
    and returns the authenticated user.
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        token_data = TokenPayload(
            user_id=payload.get("user_id"),
            role=payload.get("role"),
            expiration_time=payload.get("exp") or payload.get("expiration_time"),
        )

        if datetime.now(tz=timezone.utc).timestamp() > float(token_data.expiration_time):
            raise TokenExpiredError()

    except ExpiredSignatureError:
        raise TokenExpiredError()

    except InvalidSignatureError:
        # Token signature invalid means token was tampered or wrong KEY used
        raise InvalidTokenError("Invalid token signature.")

    except InvalidTokenError:
        # Token structure invalid
        raise InvalidEmailError()

    # Lookup user from DB
    try:
        user = get_user_by_id_service(db, int(token_data.user_id))
    except Exception:
        raise UserNotFoundError()

    return user
