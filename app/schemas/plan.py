import uuid
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PlanCreate(BaseModel):
    router_id:        uuid.UUID
    name:             str
    price_ugx:        int
    duration_hours:   int
    speed_limit:      str
    mikrotik_profile: str


class PlanUpdate(BaseModel):
    name:             Optional[str]  = None
    price_ugx:        Optional[int]  = None
    duration_hours:   Optional[int]  = None
    speed_limit:      Optional[str]  = None
    mikrotik_profile: Optional[str]  = None
    is_active:        Optional[bool] = None


class PlanResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:               uuid.UUID
    router_id:        uuid.UUID
    name:             str
    price_ugx:        int
    duration_hours:   int
    speed_limit:      str
    mikrotik_profile: str
    is_active:        bool
    created_at:       datetime