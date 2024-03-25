from datetime import timedelta, datetime
from typing import Any, TypeVar

import jwt
from passlib.context import CryptContext

from app.core.config import settings
from app.db.mongo_db import refresh_token_collection
from app.repository.refresh_repository import refresh_token_repository

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_access_token(
        username, **kwargs
) -> str:
    return generate_jwt_token(
        data={"username": username, **kwargs},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(
        username, **kwargs
) -> str:
    refresh_token = generate_jwt_token(
        data={"username": username, **kwargs},
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    )

    inserted = refresh_token_repository.save_refresh_key(username, refresh_token)

    if not inserted:
        raise ValueError("Cannot insert refresh token")

    return refresh_token


def generate_jwt_token(data: dict, expires_delta: timedelta = None, **kwargs) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, **data, **kwargs}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


T = TypeVar('T')


def extract_jwt_token(token: str, response_type: T = Any) -> T:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise ValueError("Token is expired")
    except jwt.InvalidTokenError:
        raise ValueError("Invalid token")
