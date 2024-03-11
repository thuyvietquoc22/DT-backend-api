from datetime import timedelta, datetime
from typing import Any

import jwt
from passlib.context import CryptContext

from app.core.config import settings

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
    return generate_jwt_token(
        data={"username": username, **kwargs},
        expires_delta=timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    )


def generate_jwt_token(data: dict, expires_delta: timedelta = None, **kwargs) -> str:
    expire = datetime.utcnow() + expires_delta
    to_encode = {"exp": expire, **data, **kwargs}
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
