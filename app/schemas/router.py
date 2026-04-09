import uuid
from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class RouterCreate(BaseModel):
    name:         str
    location:     Optional[str] = None
    wg_ip:        Optional[str] = None
    api_username: str
    api_password: str
    api_port:     int = 8728


class RouterUpdate(BaseModel):
    name:         Optional[str]  = None
    location:     Optional[str]  = None
    wg_ip:        Optional[str]  = None
    api_username: Optional[str]  = None
    api_password: Optional[str]  = None
    api_port:     Optional[int]  = None
    is_active:    Optional[bool] = None


class RouterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id:           uuid.UUID
    name:         str
    location:     Optional[str]
    wg_ip:        Optional[str]
    api_username: str
    api_port:     int
    is_active:    bool
    created_at:   datetime