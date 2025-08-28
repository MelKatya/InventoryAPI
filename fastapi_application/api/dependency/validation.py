from functools import wraps

from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError, ExpiredSignatureError

from security.jwt_utils import decoded_jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def validate_token_type(token_type: str, payload: dict):
    current_token_type = payload.get("type")
    if token_type == current_token_type:
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid token type {current_token_type} "
                   f"expected {token_type}"
        )

def validate_refresh_token(refresh_token: str = Cookie()):
    payload = decoded_jwt(refresh_token)
    validate_token_type("refresh", payload)
    return payload


def validate_access_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = decoded_jwt(token)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token error"
        )
    validate_token_type("access", payload)
    return payload


def validate_roles(roles: set[str]):

    def wrapper(func):
        @wraps(func)
        async def validate(*args, **kwargs):
            payload: dict | None = kwargs.get("payload")
            if not payload:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid token error"
                )

            current_roles = set(payload.get("roles"))
            if not roles.intersection(current_roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="No roles allowed"
                )

            return await func(*args, **kwargs)
        return validate
    return wrapper
