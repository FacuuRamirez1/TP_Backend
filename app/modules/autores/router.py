from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.autores import service
from app.modules.autores.schemas import AutorCreate, AutorRead, AutorUpdate
from app.modules.libros.schemas import LibroAutorRead

router = APIRouter(prefix="/autores", tags=["autores"])


@router.post("/", response_model=AutorRead, status_code=status.HTTP_201_CREATED)
async def create(data: AutorCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await service.create(session, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get("/{item_id}", response_model=AutorRead)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await service.get(session, item_id)
    if item is None:
        raise HTTPException(404, "Autor no encontrado")
    return item


@router.patch("/{item_id}", response_model=AutorRead)
async def update(item_id: int, data: AutorUpdate, session: AsyncSession = Depends(get_session)):
    try:
        item = await service.update(session, item_id, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    if item is None:
        raise HTTPException(404, "Autor no encontrado")
    return item


@router.get("/{item_id}/libros", response_model=list[LibroAutorRead])
async def list_books(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await service.get(session, item_id)
    if item is None:
        raise HTTPException(404, "Autor no encontrado")
    return item.autorias
