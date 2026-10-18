from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.modules.generos.models import Genero
from app.modules.generos.schemas import GeneroCreate


async def create(session: AsyncSession, data: GeneroCreate) -> Genero:
    item = Genero(**data.model_dump())
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Ya existe un género con ese nombre") from exc
    await session.refresh(item)
    return item


async def list_all(session: AsyncSession, limit: int, offset: int) -> list[Genero]:
    result = await session.execute(select(Genero).options(selectinload(Genero.libros)).offset(offset).limit(limit))
    return list(result.scalars().unique())


async def get(session: AsyncSession, item_id: int) -> Genero | None:
    return (await session.execute(select(Genero).options(selectinload(Genero.libros)).where(Genero.id == item_id))).scalar_one_or_none()
