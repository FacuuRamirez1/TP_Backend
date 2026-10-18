from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.modules.editoriales.models import Editorial
from app.modules.libros.models import Libro


async def create(session: AsyncSession, data) -> Editorial:
    item = Editorial(**data.model_dump())
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Ya existe una editorial con ese nombre") from exc
    await session.refresh(item)
    return item


async def list_all(session: AsyncSession, limit: int, offset: int) -> list[Editorial]:
    result = await session.execute(
        select(Editorial).options(selectinload(Editorial.libros)).offset(offset).limit(limit)
    )
    return list(result.scalars().unique())


async def get(session: AsyncSession, item_id: int) -> Editorial | None:
    return (
        await session.execute(
            select(Editorial).options(selectinload(Editorial.libros)).where(Editorial.id == item_id)
        )
    ).scalar_one_or_none()


async def update(session: AsyncSession, item_id: int, data) -> Editorial | None:
    item = await get(session, item_id)
    if item is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Ya existe una editorial con ese nombre") from exc
    await session.refresh(item)
    return item


async def books(session: AsyncSession, item_id: int) -> tuple[Editorial | None, list[Libro]]:
    item = await get(session, item_id)
    return (None, []) if item is None else (item, item.libros)
