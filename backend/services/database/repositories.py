from datetime import date, datetime, timedelta
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.model.request import SaveRequestModel
from backend.services.database.tables import TicketHistory
from backend.utils.enums import ResponseCategories, Priorities


class TicketHistoryRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, request: SaveRequestModel):
        self._session.add(TicketHistory(**request.model_dump()))

    # by id
    async def get_by_id(self, id_: int):
        query = select(TicketHistory).where(TicketHistory.id == id_)
        stmt = await self._session.execute(query)
        return stmt.scalar_one_or_none()

    # с фильтрацией
    async def get(
            self,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None,
            category: Optional[ResponseCategories] = None,
            priority: Optional[Priorities] = None,
    ):
        query = select(TicketHistory)
        if start_date is not None:
            query = query.where(TicketHistory.created_at >= datetime.combine(start_date, datetime.min.time()))
        if end_date is not None:
            query = query.where(
                TicketHistory.created_at < datetime.combine(end_date, datetime.min.time()) + timedelta(days=1)
            )
        if category is not None:
            query = query.where(TicketHistory.category == category)
        if priority is not None:
            query = query.where(TicketHistory.priority == priority)
        stmt = await self._session.execute(query)
        return stmt.scalars().all()
