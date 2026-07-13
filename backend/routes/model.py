from fastapi import APIRouter
from backend.schemas.model.request import ModelRequest
from backend.schemas.model.response import ModelResponse

router = APIRouter(prefix="/model", tags=["Model", 'Модель'])

@router.post("/", response_model=ModelResponse)
async def get_model_response(request: ModelRequest):
    ...