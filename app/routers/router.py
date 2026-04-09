"""Router endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.router import RouterCreate, RouterUpdate, RouterResponse
from app.services import router_service


router = APIRouter(prefix="/routers", tags=["Routers"])


@router.post("/", response_model=RouterResponse, status_code=status.HTTP_201_CREATED)
async def create_router(
    router_in: RouterCreate,
    db: AsyncSession = Depends(get_db)
):
    """Create a new router."""
    return await router_service.create_router(router_in, db)


@router.get("/", response_model=list[RouterResponse])
async def list_routers(db: AsyncSession = Depends(get_db)):
    """Return all routers."""
    return await router_service.list_routers(db)


@router.get("/{router_id}", response_model=RouterResponse)
async def get_router(
    router_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Get a single router by ID."""
    return await router_service.get_router(router_id, db)


@router.patch("/{router_id}", response_model=RouterResponse)
async def update_router(
    router_id: str,
    router_in: RouterUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Update a router by ID."""
    return await router_service.update_router(router_id, router_in, db)


@router.delete("/{router_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_router(
    router_id: str,
    db: AsyncSession = Depends(get_db)
):
    """Delete a router by ID."""
    await router_service.delete_router(router_id, db)