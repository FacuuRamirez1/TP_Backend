from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.modules.libros.models import Libro, LibroAutor


def options():
    return (
        joinedload(Libro.editorial),
        joinedload(Libro.genero),
        selectinload(Libro.autorias).joinedload(LibroAutor.autor),
    )


async def create(session: AsyncSession, data) -> Libro:
    item = Libro(
        isbn=data.isbn, titulo=data.titulo, precio=data.precio, stock=data.stock,
        editorial_id=data.editorial_id, genero_id=data.genero_id,
        autorias=[LibroAutor(**author.model_dump()) for author in data.autores],
    )
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("El libro contiene datos duplicados o referencias inexistentes") from exc
    return await get(session, item.id)


async def list_all(session: AsyncSession, limit: int, offset: int, titulo: str | None, genero_id: int | None):
    query = select(Libro).options(*options()).offset(offset).limit(limit)
    if titulo:
        query = query.where(Libro.titulo.ilike(f"%{titulo}%"))
    if genero_id is not None:
        query = query.where(Libro.genero_id == genero_id)
    return list((await session.execute(query)).scalars().unique())


async def get(session: AsyncSession, item_id: int) -> Libro | None:
    return (await session.execute(select(Libro).options(*options()).where(Libro.id == item_id))).scalar_one_or_none()


async def update(session: AsyncSession, item_id: int, data) -> Libro | None:
    item = await get(session, item_id)
    if item is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("El libro contiene datos duplicados o referencias inexistentes") from exc
    return await get(session, item_id)
