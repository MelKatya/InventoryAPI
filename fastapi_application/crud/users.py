from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from core.models import User, UserRole, Role
from core.schemas.user import UserCreate


async def create_user(session: AsyncSession, new_user: UserCreate):
    user = User(**new_user.model_dump(exclude={"role_id"}))
    session.add(user)
    await session.flush()
    await add_role_to_user(
        session=session,
        user_id=user.id,
        roles_id=new_user.role_id,
    )
    await session.commit()
    return user


async def add_role_to_user(
    session: AsyncSession,
    user_id: int,
    roles_id: list[int],
):
    new_some = [UserRole(user_id=user_id, role_id=role) for role in roles_id]
    session.add_all(new_some)
    await session.commit()

async def get_user_roles(
    session: AsyncSession,
    user_id: int,
):
    stmt = select(Role.name).join(Role.users_roles).filter_by(user_id=user_id)
    result = await session.scalars(stmt)
    return result.all()


async def get_all_users(session: AsyncSession):
    stmt = select(User).options(selectinload(User.users_roles).selectinload(UserRole.roles)).order_by(User.id)
    result = await session.scalars(stmt)
    return result.all()


async def get_user_by_username(session: AsyncSession, username: str):
    stmt = select(User).filter_by(username=username)
    result = await session.scalars(stmt)
    return result.one_or_none()
