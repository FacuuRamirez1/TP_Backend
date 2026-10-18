from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.libros import service
from app.modules.libros.schemas import LibroCreate, LibroRead, LibroUpdate

router = APIRouter(prefix="/libros", tags=["libros"])


@router.post("/", response_model=LibroRead, status_code=status.HTTP_201_CREATED)
async def create(data: LibroCreate, session: AsyncSession = Depends(get_session)):
    try:
        return await service.create(session, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get("/", response_model=list[LibroRead])
async def list_items(
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    titulo: str | None = None,
    genero_id: int | None = Query(None, gt=0),
    session: AsyncSession = Depends(get_session),
):
    return await service.list_all(session, limit, offset, titulo, genero_id)


@router.get("/{item_id}", response_model=LibroRead)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    item = await service.get(session, item_id)
    if item is None:
        raise HTTPException(404, "Libro no encontrado")
    return item


@router.patch("/{item_id}", response_model=LibroRead)
async def update(
    item_id: int, data: LibroUpdate, session: AsyncSession = Depends(get_session)
):
    try:
        item = await service.update(session, item_id, data)
    except ValueError as exc:
        raise HTTPException(409, str(exc)) from exc
    if item is None:
        raise HTTPException(404, "Libro no encontrado")
    return item
