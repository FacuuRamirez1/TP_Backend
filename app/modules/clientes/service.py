from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.modules.clientes.models import Cliente, PerfilCliente
from app.modules.ventas.models import Venta


async def create(session: AsyncSession, data) -> Cliente:
    item = Cliente(**data.model_dump())
    session.add(item)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Ya existe un cliente con ese email") from exc
    await session.refresh(item)
    return item


async def get(session: AsyncSession, item_id: int) -> Cliente | None:
    return (await session.execute(select(Cliente).options(joinedload(Cliente.perfil)).where(Cliente.id == item_id))).scalar_one_or_none()


async def update(session: AsyncSession, item_id: int, data) -> Cliente | None:
    item = await get(session, item_id)
    if item is None:
        return None
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("Ya existe un cliente con ese email") from exc
    return await get(session, item_id)


async def add_profile(session: AsyncSession, client_id: int, data) -> PerfilCliente | None:
    client = await get(session, client_id)
    if client is None:
        return None
    profile = PerfilCliente(cliente_id=client_id, **data.model_dump())
    session.add(profile)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("El cliente ya tiene un perfil") from exc
    await session.refresh(profile)
    return profile


async def sales(session: AsyncSession, client_id: int) -> tuple[Cliente | None, list[Venta]]:
    client = await get(session, client_id)
    if client is None:
        return None, []
    result = await session.execute(select(Venta).where(Venta.cliente_id == client_id).options(joinedload(Venta.cliente), selectinload(Venta.renglones)))
    return client, list(result.scalars().unique())
