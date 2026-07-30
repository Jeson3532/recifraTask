from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, Path, Query
from backend.schemas.model.request import ModelRequest, GetTicketFilteredModel, SaveRequestModel
from backend.schemas.model.response import ModelResponse
from backend.dependencies.state import get_model
from backend.dependencies.services import get_ticket_service
from backend.services.database.service import TicketHistoryService
from backend.services.ml.engine import ModelService
from backend.dependencies.security import authorize
from backend.utils.enums import ResponseCategories, Priorities

router = APIRouter(prefix="/support", tags=["Support", 'Поддержка'])


def get_ticket_filter(
        start_date: Optional[date] = Query(None),
        end_date: Optional[date] = Query(None),
        category: Optional[ResponseCategories] = Query(None),
        priority: Optional[Priorities] = Query(None),
) -> GetTicketFilteredModel:
    return GetTicketFilteredModel(
        start_date=start_date,
        end_date=end_date,
        category=category,
        priority=priority,
    )


@router.post("/review-classifier", response_model=ModelResponse)
async def get_model_response(
        request: ModelRequest,
        ticket_service: TicketHistoryService = Depends(get_ticket_service),
        model: ModelService = Depends(get_model),
        _auth: None = Depends(authorize)):
    answer = model.request(request.text)
    # сохранение тикета
    await ticket_service.add_ticket(SaveRequestModel(request_text=request.text, **answer))
    return answer


@router.get("/ticket")
async def get_ticket_by_filter(
        request_filter: GetTicketFilteredModel = Depends(get_ticket_filter),
        service: TicketHistoryService = Depends(get_ticket_service),
        _auth: None = Depends(authorize)):
    return await service.get_ticket_filtered(filter=request_filter)


@router.get("/ticket/{id}")
async def get_ticket_by_id(
        id: int = Path(...),
        service: TicketHistoryService = Depends(get_ticket_service),
        _auth: None = Depends(authorize)):
    return await service.get_ticket_by_id(id=id)
