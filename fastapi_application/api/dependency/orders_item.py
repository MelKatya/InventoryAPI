from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import db_helper, OrderItem
from crud.order_item import get_item_by_id


async def item_by_id(
    item_id: Annotated[int, Path],
    session: AsyncSession = Depends(db_helper.session_getter),
) -> OrderItem:
    item = await get_item_by_id(item_id=item_id, session=session)

    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item {item_id} not found"
        )

    return item
