"""Modulo de health.

Todo el modulo vive en un unico archivo: el DTO de salida (``HealthRead``), la
logica de comprobacion (``check_database``) y las rutas HTTP (``router``).

- ``GET /health/live`` no toca la base y siempre responde 200.
- ``GET /health/ready`` ejecuta ``SELECT 1``; si la base no responde devuelve 503.
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_session


class HealthRead(BaseModel):
    """DTO de salida del estado de la aplicacion."""

    estado: str


async def check_database(session: AsyncSession) -> bool:
    """Ejecuta una consulta trivial para verificar que la base responde."""

    await session.execute(text("SELECT 1"))
    return True


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
