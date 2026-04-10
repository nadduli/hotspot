from sqlalchemy import ForeignKey, String, Boolean, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column
import uuid

from app.db.database import Base


class Plan(Base):
    """Internet plans available for purchase."""

    router_id:        Mapped[uuid.UUID] = mapped_column(ForeignKey("routers.id"), nullable=False)
    name:             Mapped[str]       = mapped_column(String,  nullable=False)
    price_ugx:        Mapped[int]       = mapped_column(Integer, nullable=False)
    duration_hours:   Mapped[int]       = mapped_column(Integer, nullable=False)
    speed_limit:      Mapped[str]       = mapped_column(String,  nullable=False, default="2M/2M")
    mikrotik_profile: Mapped[str]       = mapped_column(String,  nullable=False)
    is_active:        Mapped[bool]      = mapped_column(Boolean, nullable=False, default=True)

    router: Mapped["Router"] = relationship("Router", back_populates="plans")

    def __repr__(self) -> str:
        return f"<Plan {self.name} | {self.price_ugx} UGX | active={self.is_active}>"