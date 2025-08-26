from datetime import timedelta

from core.config import settings
from core.models import User
from security.jwt_utils import encode_jwt


def create_jwt(
    token_type: str,
    token_data: dict,
    expire: timedelta,
):
    jwt_payload = {"type": token_type}
    jwt_payload.update(token_data)
    return encode_jwt(payload=jwt_payload, expire_timedelta=expire)


def create_access_token(user: User, roles: list[str]):
    jwt_payload = {"sub": str(user.id), "roles": roles}
    expire = timedelta(minutes=settings.jwt.access_token_expire_minutes)
    return create_jwt(
        token_type="access",
        token_data=jwt_payload,
        expire=expire
    )


def create_refresh_token(user: User):
    jwt_payload = {"sub": user.id}
    expire = timedelta(days=settings.jwt.refresh_token_expire_days)
    return create_jwt(
        token_type="refresh",
        token_data=jwt_payload,
        expire=expire
    )