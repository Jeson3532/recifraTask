from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.types import Integer, String, Enum, Float, JSON
from sqlalchemy.dialects.postgresql import JSONB
from backend.utils.enums import Priorities, ResponseCategories
from sqlalchemy import func
from datetime import datetime
from typing import Dict


class Base(DeclarativeBase):
    ...


class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_text: Mapped[str] = mapped_column(String(1024), nullable=False)
    category: Mapped[ResponseCategories] = mapped_column(Enum(ResponseCategories), nullable=False)
    priority: Mapped[Priorities] = mapped_column(Enum(Priorities), nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False)
    probabilities: Mapped[Dict[str, float]] = mapped_column(JSONB, nullable=False)

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
