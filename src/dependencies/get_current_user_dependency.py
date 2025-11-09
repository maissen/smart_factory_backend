from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.services.user.get_user_by_id_service import get_user_by_id_service
from sqlalchemy.orm import Session
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timezone

from src.dependencies.postgres_dependency import get_db
from src.schema.token_schema import TokenPayload
from src.core.settings import settings
from src.exceptions.user_exceptions import *
from src.exceptions.token_exceptions import *

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")  # login route

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    
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

        if datetime.now(tz=timezone.utc).timestamp() > token_data.expiration_time:
            raise TokenExpiredError()

    except ExpiredSignatureError:
        raise TokenExpiredError()
    
    except InvalidTokenError:
        raise InvalidEmailError()

    # Fetch user by ID
    try:
        user = get_user_by_id_service(db, int(token_data.user_id))

    except Exception as e:
        raise UserNotFoundError()



    return user

