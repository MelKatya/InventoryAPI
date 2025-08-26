from functools import wraps

from fastapi import Depends, HTTPException, status
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


