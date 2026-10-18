from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.editoriales import service
from app.modules.editoriales.schemas import EditorialCreate, EditorialRead, EditorialUpdate
from app.modules.libros.schemas import LibroListRead

router = APIRouter(prefix="/editoriales", tags=["editoriales"])


@router.post("/", response_model=EditorialRead, status_code=status.HTTP_201_CREATED)
async def create(data: EditorialCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await service.create(session, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get("/", response_model=list[EditorialRead])
async def list_items(
    limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_all(session, limit, offset)


@router.get("/{item_id}", response_model=EditorialRead)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await service.get(session, item_id)
    if item is None:
        raise HTTPException(404, "Editorial no encontrada")
    return item


@router.patch("/{item_id}", response_model=EditorialRead)
async def update(item_id: int, data: EditorialUpdate, session: AsyncSession = Depends(get_session)):
    try:
        item = await service.update(session, item_id, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    if item is None:
        raise HTTPException(404, "Editorial no encontrada")
    return item


@router.get("/{item_id}/libros", response_model=list[LibroListRead])
async def list_books(item_id: int, session: AsyncSession = Depends(get_session)):
    item, books = await service.books(session, item_id)
    if item is None:
        raise HTTPException(404, "Editorial no encontrada")
    return books
