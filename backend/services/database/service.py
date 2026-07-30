from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.model.request import SaveRequestModel, GetTicketFilteredModel
import logging

from .repositories import TicketHistoryRepo

logger = logging.getLogger(__name__)


class DatabaseService:

    def __init__(self, session: AsyncSession):
        self._session = session
        self.ticket_history = TicketHistoryRepo(session)

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()

    async def refresh(self, obj):
        await self._session.refresh(obj)

    async def execute(self, sql):
        return await self._session.execute(sql)


class TicketHistoryService:
    def __init__(self, db: DatabaseService):
        self._db = db

    async def add_ticket(self, request_data: SaveRequestModel):
        try:
            self._db.ticket_history.add(request=request_data)
            await self._db.commit()
        except Exception as e:
            await self._db.rollback()
            logger.error(f"Ошибка в {self.__class__.__name__}. Traceback: {e}", exc_info=True)
            raise

    async def get_ticket_by_id(self, id: int):
        try:
            return await self._db.ticket_history.get_by_id(id_=id)
        except Exception as e:
            logger.error(f"Ошибка в {self.__class__.__name__}. Traceback: {e}", exc_info=True)
            raise

    async def get_ticket_filtered(self, filter: GetTicketFilteredModel):
        try:
            return await self._db.ticket_history.get(**filter.model_dump())
        except Exception as e:
            logger.error(f"Ошибка в {self.__class__.__name__}. Traceback: {e}", exc_info=True)
            raise
