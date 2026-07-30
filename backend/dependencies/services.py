from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.services.database.service import DatabaseService, TicketHistoryService
from backend.services.database.engine import get_session


def get_db_service(session: AsyncSession = Depends(get_session)):
    return DatabaseService(session=session)


def get_ticket_service(db: DatabaseService = Depends(get_db_service)):
    return TicketHistoryService(db=db)
