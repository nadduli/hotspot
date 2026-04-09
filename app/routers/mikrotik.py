"""MikroTik connection routes."""

import asyncio
from functools import partial

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services import router_service, mikrotik_service

router = APIRouter(prefix="/routers", tags=["MikroTik"])


@router.get("/{router_id}/test-connection")
async def test_router_connection(
    router_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Test the live connection to a MikroTik router."""
    db_router = await router_service.get_router(router_id, db)

    loop   = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None,
        partial(mikrotik_service.test_connection, db_router)
    )
    return result

