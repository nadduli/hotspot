"""Application entry point."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.core.config import settings
from app.core.logging import setup_logging
from app.db.database import engine, Base
from app.routers.router import router as router_router
from app.routers.mikrotik import router as mikrotik_router


logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging(debug=settings.DEBUG)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    logger.info(f"Application started | debug={settings.DEBUG}")

    yield

    await engine.dispose()
    logger.info("Application shutdown complete")


app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.DEBUG,
    lifespan=lifespan
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(router_router)
app.include_router(mikrotik_router)


@app.get("/health")
async def health():
    return {"status": "ok", "app": settings.APP_NAME}