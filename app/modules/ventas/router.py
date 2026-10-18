from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.ventas import service
from app.modules.ventas.schemas import VentaCreate, VentaRead, VentaListRead

router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.post("/", response_model=VentaRead, status_code=status.HTTP_201_CREATED)
async def create(data: VentaCreate, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_session)):
    try:
        sale = await service.create(session, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    background_tasks.add_task(service.notify_receipt, data.cliente_id, sale.id)
    return sale


@router.get("/", response_model=list[VentaListRead])
async def list_items(limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0), session: AsyncSession = Depends(get_session)):
    return await service.list_all(session, limit, offset)


@router.get("/{item_id}", response_model=VentaRead)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    sale = await service.get(session, item_id)
    if sale is None:
        raise HTTPException(404, "Venta no encontrada")
    return sale
