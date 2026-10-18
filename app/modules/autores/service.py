from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.autores.models import Autor
from app.modules.libros.models import LibroAutor


async def create(session: AsyncSession, data) -> Autor:
    item = Autor(**data.model_dump())
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("No se pudo crear el autor") from exc
    await session.refresh(item)
    return item


async def get(session: AsyncSession, item_id: int) -> Autor | None:
    return (
        await session.execute(
            select(Autor)
            .options(selectinload(Autor.autorias).joinedload(LibroAutor.libro))
            .where(Autor.id == item_id)
        )
    ).scalar_one_or_none()


async def update(session: AsyncSession, item_id: int, data) -> Autor | None:
    item = await get(session, item_id)
    if item is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("No se pudo actualizar el autor") from exc
    await session.refresh(item)
    return item
