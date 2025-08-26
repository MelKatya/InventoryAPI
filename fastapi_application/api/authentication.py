from fastapi import APIRouter, Depends, HTTPException, status, Form, Response
from sqlalchemy.ext.asyncio import AsyncSession

from api.validation import validate_access_token, validate_roles, validate_refresh_token
from core.models import db_helper, User
from core.schemas.token import TokenInfo
from crud import users as crud_us
from crud.users import get_user_roles, get_user_by_id
from security.hashed_utils import validate_password
from security.jwt_create import create_access_token, create_refresh_token



router = APIRouter(tags=["Auth"])

@router.post("/login")
async def auth_user_jwt(
    response: Response,
    username: str = Form(),
    password: str = Form(),
    session: AsyncSession = Depends(db_helper.session_getter),
) -> TokenInfo:
    authed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
    )

    user: User = await crud_us.get_user_by_username(
        session=session,
        username=username,
    )

    if not user:
        raise authed_exc

    if not validate_password(
            password=password,
            hashed_password=user.hashed_password.encode()
    ):
        raise authed_exc

    roles = await get_user_roles(session=session, user_id=user.id)
    access_token = create_access_token(user, roles)
    refresh_token = create_refresh_token(user)
    response.set_cookie(key="refresh_token", value=refresh_token)

    return TokenInfo(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout_user(
    response: Response,
    refresh_token: dict = Depends(validate_refresh_token),
    access_token: dict = Depends(validate_access_token),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    response.delete_cookie("refresh_token")
    user_id = int(access_token.get("sub"))
    user = await get_user_by_id(session, user_id)
    return {"Bye": user.username}


@router.post("/refresh")
async def auth_refresh_jwt(
    token: dict = Depends(validate_access_token),
):
    print(token)
    return {"token": "sks"}


@router.get("/me")
async def auth_user_check_self_info():
    ...

