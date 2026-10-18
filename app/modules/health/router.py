from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session
from app.modules.health.schemas import HealthRead
from app.modules.health.service import check_database

router = APIRouter(prefix="/health", tags=["health"])


@router.get("/live", response_model=HealthRead)
async def live() -> HealthRead:
    return HealthRead(estado="vivo")


@router.get("/ready", response_model=HealthRead)
async def ready(session: AsyncSession = Depends(get_session)) -> HealthRead:
    try:
        await check_database(session)
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Base de datos no disponible") from exc
    return HealthRead(estado="listo")
