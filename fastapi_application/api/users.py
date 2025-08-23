from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.models import db_helper
from core.schemas.user import UserCreateGet, UserCreate
from security.hashed_pass import hash_password
from crud import users as crud_us

router = APIRouter(tags=["Users"])


@router.post("/create")
async def create_user(
        user: UserCreateGet,
        session: AsyncSession = Depends(db_helper.session_getter)
):
    hashed_password = hash_password(user.password)
    roles_id = [settings.mappings.roles.get(role) for role in user.role]
    new_user = UserCreate(
        **user.model_dump(),
        hashed_password=hashed_password.decode(),
        role_id=roles_id
    )
    created_user = await crud_us.create_user(new_user=new_user, session=session)
    return created_user


@router.get("")
async def get_all_users(
        session: AsyncSession = Depends(db_helper.session_getter),
):
    all_users = await crud_us.get_all_users(session)
    return all_users


@router.get("/{user_id}")
async def get_user_by_id():
    ...


@router.patch("/{user_id}")
async def update_user_data():
    ...




