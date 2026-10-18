from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import create_database_resources
from app.modules.autores.router import router as autores_router
from app.modules.clientes.router import router as clientes_router
from app.modules.editoriales.router import router as editoriales_router
from app.modules.generos.router import router as generos_router
from app.modules.health.router import router as health_router
from app.modules.libros.router import router as libros_router
from app.modules.ventas.router import router as ventas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine, session_maker = create_database_resources()
    app.state.engine = engine
    app.state.session_maker = session_maker
    yield
    await engine.dispose()


app = FastAPI(title="Librería API", lifespan=lifespan)
for router in (
    health_router, editoriales_router, generos_router, autores_router,
    libros_router, clientes_router, ventas_router,
):
    app.include_router(router)
