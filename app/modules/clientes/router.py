from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.clientes import service
from app.modules.clientes.schemas import ClienteCreate, ClienteRead, ClienteUpdate, PerfilCreate, PerfilRead
from app.modules.ventas.schemas import VentaListRead

router = APIRouter(prefix="/clientes", tags=["clientes"])


@router.post("/", response_model=ClienteRead, status_code=status.HTTP_201_CREATED)
async def create(data: ClienteCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await service.create(session, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get("/{item_id}", response_model=ClienteRead)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await service.get(session, item_id)
    if item is None:
        raise HTTPException(404, "Cliente no encontrado")
    return item


@router.patch("/{item_id}", response_model=ClienteRead)
async def update(item_id: int, data: ClienteUpdate, session: AsyncSession = Depends(get_session)):
    try:
        item = await service.update(session, item_id, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    if item is None:
        raise HTTPException(404, "Cliente no encontrado")
    return item


@router.post("/{item_id}/perfil", response_model=PerfilRead, status_code=status.HTTP_201_CREATED)
async def add_profile(item_id: int, data: PerfilCreate, session: AsyncSession = Depends(get_session)):
    try:
        profile = await service.add_profile(session, item_id, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    if profile is None:
        raise HTTPException(404, "Cliente no encontrado")
    return profile


@router.get("/{item_id}/ventas", response_model=list[VentaListRead])
async def list_sales(item_id: int, session: AsyncSession = Depends(get_session)):
    client, sales = await service.sales(session, item_id)
    if client is None:
        raise HTTPException(404, "Cliente no encontrado")
    return sales
