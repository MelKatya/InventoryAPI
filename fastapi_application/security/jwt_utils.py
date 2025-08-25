from datetime import timedelta, datetime

import jwt

from core.config import settings


def encode_jwt(
    expire_timedelta: timedelta,
    payload: dict,
    private_key: str = settings.jwt.private_key.read_text(),
    algorithm: str = settings.jwt.algorithm,
):
    to_encode = payload.copy()
    expire = datetime.now() + expire_timedelta
    to_encode.update(exp=expire)

    encoded = jwt.encode(
        payload=to_encode,
        key=private_key,
        algorithm=algorithm
    )
    return encoded


def decoded_jwt(
    token: str | bytes,
    public_key: str = settings.jwt.public_key.read_text(),
    algorithm: str = settings.jwt.algorithm,
):
    decoded = jwt.decode(
        jwt=token,
        key=public_key,
        algorithms=[algorithm]
    )
    return decoded
