import asyncio
import logging
from collections.abc import Awaitable
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from app.modules.clientes.models import Cliente
from app.modules.libros.models import Libro
from app.modules.ventas.models import RenglonVenta, Venta

logger = logging.getLogger(__name__)


async def notify_receipt(client_id: int, sale_id: int) -> None:
    await asyncio.sleep(0.5)
    logger.info("Aviso de comprobante enviado al cliente %s para la venta %s", client_id, sale_id)


def options():
    return (
        joinedload(Venta.cliente).joinedload(Cliente.perfil),
        selectinload(Venta.renglones).joinedload(RenglonVenta.libro),
    )


async def create(session: AsyncSession, data) -> Venta:
    client = await session.get(Cliente, data.cliente_id)
    if client is None:
        raise ValueError("El cliente indicado no existe")
    books = {}
    for row in data.renglones:
        book = await session.get(Libro, row.libro_id)
        if book is None:
            raise ValueError("Uno de los libros indicados no existe")
        books[row.libro_id] = book
    lines = [RenglonVenta(libro_id=row.libro_id, cantidad=row.cantidad, precio_unitario=books[row.libro_id].precio) for row in data.renglones]
    total = sum((line.precio_unitario * line.cantidad for line in lines), Decimal("0.00"))
    sale = Venta(cliente_id=data.cliente_id, total=total, renglones=lines)
    session.add(sale)
    try:
        await session.commit()
    except IntegrityError as exc:
        await session.rollback()
        raise ValueError("No se pudo registrar la venta por datos inválidos") from exc
    return await get(session, sale.id)


async def list_all(session: AsyncSession, limit: int, offset: int):
    result = await session.execute(select(Venta).options(*options()).offset(offset).limit(limit))
    return list(result.scalars().unique())


async def get(session: AsyncSession, item_id: int) -> Venta | None:
    return (await session.execute(select(Venta).options(*options()).where(Venta.id == item_id))).scalar_one_or_none()
