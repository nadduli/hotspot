from typing import Optional
from sqlalchemy import String, Integer, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from .plan import Plan


class Router(Base):
    """Represents a MikroTik router stored in the database."""

    name:         Mapped[str]           = mapped_column(String,  nullable=False)
    location:     Mapped[Optional[str]] = mapped_column(String,  nullable=True)
    wg_ip:        Mapped[Optional[str]] = mapped_column(String,  nullable=True)
    api_username: Mapped[str]           = mapped_column(String,  nullable=False)
    api_password: Mapped[str]           = mapped_column(String,  nullable=False)
    api_port:     Mapped[int]           = mapped_column(Integer, nullable=False,  default=8728)
    is_active:    Mapped[bool]          = mapped_column(Boolean, nullable=False,  default=True)

    plans: Mapped[list["Plan"]] = relationship("Plan", back_populates="router")

    def __repr__(self) -> str:
        return f"<Router {self.name} | {self.wg_ip} | active={self.is_active}>"