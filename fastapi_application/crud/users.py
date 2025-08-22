from sqlalchemy.ext.asyncio import AsyncSession

from core.models import User, UserRole
from core.schemas.user import UserCreate


async def create_user(session: AsyncSession, new_user: UserCreate):
    user = User(**new_user.model_dump(exclude={"role_id"}))
    session.add(user)
    await session.flush()
    await add_role_to_user(session=session, user_id=user.id, roles_id=new_user.role_id)
    await session.commit()
    return user


async def add_role_to_user(session: AsyncSession, user_id: int, roles_id: list[int]):
    new_some = [UserRole(user_id=user_id, role_id=role) for role in roles_id]
    session.add_all(new_some)
    await session.commit()