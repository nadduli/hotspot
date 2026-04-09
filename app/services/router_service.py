"""Router Service — all database logic for the Router resource."""

import logging
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.router import Router
from app.schemas.router import RouterCreate, RouterUpdate


logger = logging.getLogger(__name__)


async def get_router_or_404(router_id: str, db: AsyncSession) -> Router:
    """Fetch a router by ID or raise 404."""
    result = await db.execute(select(Router).where(Router.id == router_id))
    router = result.scalar_one_or_none()

    if router is None:
        logger.warning(f"Router not found: id='{router_id}'")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Router with id '{router_id}' not found"
        )
    return router


async def create_router(router_data: RouterCreate, db: AsyncSession) -> Router:
    """Save a new router to the database."""
    new_router = Router(**router_data.model_dump(exclude_unset=True))
    db.add(new_router)
    await db.flush()
    await db.refresh(new_router)
    logger.info(f"Router created: name='{new_router.name}' id='{new_router.id}'")
    return new_router


async def list_routers(db: AsyncSession) -> list[Router]:
    """Return all routers ordered by name."""
    result = await db.execute(select(Router).order_by(Router.name))
    routers = result.scalars().all()
    logger.info(f"Listed {len(routers)} router(s)")
    return routers


async def get_router(router_id: str, db: AsyncSession) -> Router:
    """Return a single router by ID."""
    return await get_router_or_404(router_id, db)


async def update_router(
    router_id: str,
    router_data: RouterUpdate,
    db: AsyncSession
) -> Router:
    """Update only the fields that were sent in the request."""
    router = await get_router_or_404(router_id, db)
    changes = router_data.model_dump(exclude_unset=True, exclude_none=True)

    for key, value in changes.items():
        setattr(router, key, value)

    await db.flush()
    await db.refresh(router)
    logger.info(f"Router updated: id='{router_id}' fields={list(changes.keys())}")
    return router


async def delete_router(router_id: str, db: AsyncSession) -> None:
    """Permanently delete a router."""
    router = await get_router_or_404(router_id, db)
    await db.delete(router)
    await db.flush()
    logger.info(f"Router deleted: name='{router.name}' id='{router_id}'")