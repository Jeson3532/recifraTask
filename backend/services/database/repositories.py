from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.schemas.model.request import SaveRequestModel
from backend.services.database.tables import TicketHistory


class TicketHistoryRepo:
    def __init__(self, session: AsyncSession):
        self._session = session

    def add(self, request: SaveRequestModel):
        self._session.add(TicketHistory(**request.model_dump()))

    async def get_by_id(self, id_: int):
        query = select(TicketHistory).where(TicketHistory.id == id_)
        stmt = await self._session.execute(query)
        return stmt.scalar_one_or_none()
